import random

# konditionstypen: 
# 1 = wenig
# 2 = mittel
# 3
GENPOOL = {
    # Chromosomes for the Agent
    "Agent": {
        "energy": (1, 1),
        "verbrauch": (0, 1),
        "bewegungsdrang": (0, 1), #zu 20% bewegen wenn keine nahrung in sicht ist
        "chromosome4": (0, 1),
        "chromosome5": (0, 1),
    }
}

class Lebewesen:

    # distribution of Chromosomes within the Agent
    def chrom_distribution_agent(self):
        self.genetik["Ernährungstyp"] = "Agent"

        # distribute Chromosomes
        for chrom, bereich in GENPOOL["Agent"].items():
            self.genetik[chrom] = round(random.uniform(*bereich), 3)

        # access Chromosomes
        self.energy = self.genetik["energy"]
        self.chrom2 = self.genetik["chromosome2"]
        self.chrom3 = self.genetik["chromosome3"]
        self.chrom4 = self.genetik["chromosome4"]
        self.chrom5 = self.genetik["chromosome5"]


if __name__ == "__main__":

    agent = Lebewesen()
    agent.genverteilung_agent()

    print(f"Agent Chromosomes: {agent.energy}, {agent.chrom2}, {agent.chrom3}, {agent.chrom4}, {agent.chrom5}")
