# Pour lancer tous les tests faire  python -m 'Tests'
# Pour lancer un test faire         python -m 'Tests.exercice_laitues'


# Ajout du dossier pySpriteWorld dans le path
import os,sys
dossier = os.path.dirname(os.path.abspath(__file__))
while not dossier.endswith('pySpriteWorld'):
    dossier = os.path.dirname(dossier)
dossier = os.path.dirname(dossier)
if dossier not in sys.path:
    sys.path.append(dossier)

__all__ = ['exercice_laitues','correction_info2_tp3',
           'correction_info2_tp4','exercice_info2_1',
           'exercice_robot_sim']
