
# Ajout du dossier pySpriteWorld dans le path
import os
dossier = os.path.dirname(os.path.abspath(__file__))
while not dossier.endswith('pySpriteWorld'):
    dossier = os.path.dirname(dossier)
dossier = os.path.dirname(dossier)
if dossier not in sys.path:
    sys.path.append(dossier)
