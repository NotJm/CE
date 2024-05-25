from PSO import PSO
from progress.bar import Bar
from utils.limites import (boundary, reflex, random)
from utils.cec2006problems import (CEC2006_g02)
from utils.restricciones import (deb)

def main():
    pso = PSO(
        reflex,
        CEC2006_g02.CEC2006_g02_aptitud,
        deb,
        [CEC2006_g02.CEC2006_g02_g1, CEC2006_g02.CEC2006_g02_g2]
    )
    pso.report()


if __name__ == '__main__':
    main()