# DesertPatrol - mission_loader
# Autor: Arthur Martins
# Descrição: Carrega e interpreta arquivos .mission para montar o cenário de jogo

import random

class ParticleSystem(object):
    """Holds the position and name of ptf file for a particle system in a level"""
    def __init__(self, ptfFile, particlePos):
        self.ptfFile = ptfFile
        self.particlePos = particlePos

    def __repr__(self):
        return "Particle System '" + self.ptfFile + "' at " + str(self.particlePos)

class Model(object):
    """Holds the position and name of model file for a model in a level"""
    def __init__(self, modelName, modelPos):
        self.modelName = modelName
        self.modelPos = modelPos

    def __repr__(self):
        return "Model '" + self.modelName + "' at " + str(self.modelPos)

def parseMissionFile(filename):
    """Returns a list of ParticleSystem and Model objects with file names and positions of objects in the level
    from the .mission file."""
    f = open(filename, "r")
    file = f.read()
    f.close()
    models = []  #model name: pos

    for line in file.split("\n"):  #go through each line
        if not line.strip():
            continue
        lineContents = line.split(":")
        pos = lineContents[1].split(",")
        if lineContents[0].startswith("particle"):
            models.append(ParticleSystem(ptfFile = lineContents[0][8:], particlePos = (float(pos[0]), float(pos[1]), float(pos[2]))))
        else:
            models.append(Model(modelName = lineContents[0], modelPos = (float(pos[0]), float(pos[1]), float(pos[2]))))

    return models

_SPREAD = 2.5  # raio de dispersão dos objetos ao redor do centro
_GROUND_OFFSETS = {
    "cocaine-packet": 0.12,
}

def generate_random_models(model_name, count, center=(12, 22.7, 0.75)):
    """Gera `count` modelos agrupados ao redor de `center`. Sem fumaça —
    a fumaça vem do arquivo .mission e marca a posição fixa."""
    cx, cy, z = center
    z += _GROUND_OFFSETS.get(model_name, 0)
    result = []
    positions = []
    min_distance = 1.0
    attempts = 0

    while len(positions) < count and attempts < count * 30:
        attempts += 1
        x = round(cx + random.uniform(-_SPREAD, _SPREAD), 2)
        y = round(cy + random.uniform(-_SPREAD, _SPREAD), 2)
        too_close = any((x - px) ** 2 + (y - py) ** 2 < min_distance ** 2 for px, py in positions)
        if not too_close:
            positions.append((x, y))

    while len(positions) < count:
        x = round(cx + random.uniform(-_SPREAD, _SPREAD), 2)
        y = round(cy + random.uniform(-_SPREAD, _SPREAD), 2)
        positions.append((x, y))

    for x, y in positions:
        result.append(Model(modelName=model_name, modelPos=(x, y, z)))
    return result

if __name__ == "__main__":
    print(str(parseMissionFile("models/m1.mission")))
