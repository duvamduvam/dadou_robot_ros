"""Écriture NeoPixel SANS le time.sleep parasite du driver Blinka bcm283x.

POURQUOI ce module existe
-------------------------
Sur le Pi, chaque `strip.show()` de la chaîne LED (1000 LED, pin D18) coûtait
~35 ms, dont un `time.sleep(0.001 * ((len(buf) // 100) + 1))` codé EN DUR dans
`adafruit_blinka/microcontroller/bcm283x/neopixel.py` (fonction `neopixel_write`,
juste après `ws2811_render`). Pour 1000 LED × 3 octets = 3000 octets de buffer,
ce sleep vaut 31 ms — à lui seul il plafonnait le tick des nodes à ~10 Hz.

Ce sleep est INUTILE ici :
- `ws2811_render` (code C de _rpi_ws281x) attend DÉJÀ, en début d'appel, la fin
  du transfert DMA de la trame PRÉCÉDENTE avant d'en lancer une nouvelle. La
  protection anti-écrasement du buffer DMA est donc déjà dans le C ;
- le débit du fil WS2811 (~30 µs par LED) impose un plancher physique d'environ
  30 ms pour pousser 1000 LED. Deux `show()` dos à dos se régulent donc TOUT
  SEULS en C (le second bloque sur le DMA du premier) : pas besoin d'un sleep
  Python par-dessus pour « laisser le temps » à la trame de partir.

En retirant ce sleep, `show()` retombe à ~4 ms de calcul Python + l'attente DMA
réelle, ce qui a permis de monter le tick global des nodes à 20 Hz
(robot_static.TICK_PERIOD_S).

Ce qu'on garde IDENTIQUE à Blinka (fidélité : c'est du code matériel validé) :
init `ws2811_t`, boucle de conversion buf→`ws2811_led_set`, `ws2811_render`,
gestion d'erreurs, cleanup atexit. SEULE différence : le `time.sleep` final est
supprimé.

Imports matériels différés (même pattern que robot/actions/wheels.py) : ce module
doit s'importer sur x86 (collecte pytest, poste de dev). `_rpi_ws281x` n'est
importé qu'à la PREMIÈRE transmission, et `neopixel` (qui tire board/digitalio,
absents hors Pi) qu'à l'accès à la classe `FastNeoPixel` (via __getattr__).
"""

import atexit

# Configuration LED copiée VERBATIM de Blinka bcm283x — ne rien régler ici :
# on ne supporte qu'une bande 800 kHz, canal DMA 10, luminosité gérée en amont
# par la lib neopixel (le buffer reçu est DÉJÀ post-brightness).
LED_FREQ_HZ = 800000  # Fréquence du signal LED — seul 800 kHz est supporté.
LED_DMA_NUM = 10       # Canal DMA (0-14).
LED_BRIGHTNESS = 255   # Luminosité gérée dans la lib neopixel (donc 255 ici).
LED_INVERT = 0         # Pas de logique inversée.

# État « statique » : une seule bande LED par Pi. On réinitialise le contrôleur
# si le buffer d'entrée change d'identité (même logique que Blinka).
_led_strip = None
_buf = None


def _neopixel_detect_channel(pin_id):
    """Canal PWM du BCM283x pour un GPIO donné.

    Le SoC n'a que deux générateurs PWM : PWM1 est câblé sur GPIO 13/19/41/45/53
    (canal 1), PWM0 partout ailleurs (canal 0). Notre bande est sur D18 = GPIO18
    = PWM0 => canal 0. On garde la détection générique (elle est triviale) plutôt
    que de figer 0, pour rester correct si le pin change un jour.
    """
    if pin_id in (13, 19, 41, 45, 53):
        return 1
    return 0


def _fast_neopixel_write(gpio, buf):
    """Copie de `neopixel_write` (Blinka bcm283x) SANS le `time.sleep` final.

    `gpio` est un DigitalInOut (accès `gpio._pin.id`) ; `buf` est le bytearray
    post-brightness fourni par adafruit_pixelbuf. Même contrat que Blinka.
    """
    global _led_strip, _buf
    # Import différé : la lib native _rpi_ws281x n'existe que sur le Pi.
    import _rpi_ws281x as ws  # pylint: disable=import-error

    led_channel = _neopixel_detect_channel(gpio._pin.id)

    if _led_strip is None or buf is not _buf:
        # Sans danger si _led_strip est None (garde interne).
        _fast_neopixel_cleanup()

        _led_strip = ws.new_ws2811_t()
        _buf = buf

        # Initialise les deux canaux à « éteint ».
        for channum in range(2):
            channel = ws.ws2811_channel_get(_led_strip, channum)
            ws.ws2811_channel_t_count_set(channel, 0)
            ws.ws2811_channel_t_gpionum_set(channel, 0)
            ws.ws2811_channel_t_invert_set(channel, 0)
            ws.ws2811_channel_t_brightness_set(channel, 0)

        channel = ws.ws2811_channel_get(_led_strip, led_channel)

        # Initialise le canal utilisé : 3 octets/pixel (RGB) ou 4 (RGBW).
        count = 0
        if len(buf) % 3 == 0:
            strip_type = ws.WS2811_STRIP_RGB
            count = len(buf) // 3
        elif len(buf) % 4 == 0:
            strip_type = ws.SK6812_STRIP_RGBW
            count = len(buf) // 4
        else:
            raise RuntimeError("We only support 3 or 4 bytes-per-pixel")

        ws.ws2811_channel_t_count_set(channel, count)
        ws.ws2811_channel_t_gpionum_set(channel, gpio._pin.id)
        ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
        ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
        ws.ws2811_channel_t_strip_type_set(channel, strip_type)

        # Initialise le contrôleur.
        ws.ws2811_t_freq_set(_led_strip, LED_FREQ_HZ)
        ws.ws2811_t_dmanum_set(_led_strip, LED_DMA_NUM)

        resp = ws.ws2811_init(_led_strip)
        if resp != ws.WS2811_SUCCESS:
            if resp == -5:
                raise RuntimeError(
                    "NeoPixel support requires running with sudo, please try again!"
                )
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError(
                "ws2811_init failed with code {0} ({1})".format(resp, message)
            )
        atexit.register(_fast_neopixel_cleanup)

    channel = ws.ws2811_channel_get(_led_strip, led_channel)
    if gpio._pin.id != ws.ws2811_channel_t_gpionum_get(channel):
        raise RuntimeError("Raspberry Pi neopixel support is for one strip only!")

    if ws.ws2811_channel_t_strip_type_get(channel) == ws.WS2811_STRIP_RGB:
        bpp = 3
    else:
        bpp = 4

    # Conversion buffer -> pixels (identique à Blinka).
    for i in range(len(buf) // bpp):
        r = buf[bpp * i]
        g = buf[bpp * i + 1]
        b = buf[bpp * i + 2]
        if bpp == 3:
            pixel = (r << 16) | (g << 8) | b
        else:
            w = buf[bpp * i + 3]
            pixel = (w << 24) | (r << 16) | (g << 8) | b
        ws.ws2811_led_set(channel, i, pixel)

    resp = ws.ws2811_render(_led_strip)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError(
            "ws2811_render failed with code {0} ({1})".format(resp, message)
        )
    # PAS de `time.sleep(...)` ici : c'est TOUTE la raison d'être de ce module.
    # ws2811_render a déjà attendu le DMA de la trame précédente ; le fil se
    # régule seul (voir docstring du module).


def _fast_neopixel_cleanup():
    """Libère la structure ws2811_t (appelé à la sortie via atexit)."""
    global _led_strip
    if _led_strip is None:
        return
    # Import différé : cohérent avec _fast_neopixel_write (lib Pi uniquement).
    import _rpi_ws281x as ws  # pylint: disable=import-error
    ws.ws2811_fini(_led_strip)
    ws.delete_ws2811_t(_led_strip)
    _led_strip = None


def __getattr__(name):
    """Fournit `FastNeoPixel` en différé (PEP 562).

    On ne peut pas écrire `class FastNeoPixel(neopixel.NeoPixel)` au niveau module
    sans importer `neopixel` (qui tire board/digitalio, absents sur x86) et casser
    la collecte pytest. La classe n'est donc construite qu'au PREMIER accès à
    l'attribut `FastNeoPixel` — c'est-à-dire à l'instanciation côté lights_node,
    sur le Pi uniquement.
    """
    if name == "FastNeoPixel":
        import neopixel  # import différé : lib Pi (board/digitalio) absente sur x86

        class FastNeoPixel(neopixel.NeoPixel):
            """NeoPixel dont `_transmit` court-circuite le sleep de 31 ms de Blinka.

            Voir la docstring du module fast_neopixel pour le POURQUOI : le sleep
            final de `neopixel_write` est inutile (ws2811_render attend déjà le
            DMA précédent, le fil se régule seul), il plafonnait le tick à 10 Hz.
            """

            def _transmit(self, buffer):
                # Même contrat que neopixel.NeoPixel._transmit (self.pin,
                # buffer post-brightness), mais via notre écriture sans sleep.
                _fast_neopixel_write(self.pin, buffer)

        # Mémorise pour les accès suivants (évite de reconstruire la classe).
        globals()["FastNeoPixel"] = FastNeoPixel
        return FastNeoPixel

    raise AttributeError(
        "module {!r} has no attribute {!r}".format(__name__, name)
    )
