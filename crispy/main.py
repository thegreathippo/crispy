"""TODO:
    * Root's internal dict (data) uses an OrderedDict; this is because we're relying on the 'images' component for
    sprites, and if sprite is loaded on an entity before image, it creates an error. To fix this, components should
    be self-contained; sprite should contain both sprite positional data *and* image-data. Accomplishing this means
    creating a specialized dict-type -- or an internal sprite data class for the sprite component.

"""

from game import world
import gui


app = gui.GameApp(world)


app.run()
