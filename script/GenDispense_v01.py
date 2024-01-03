import random

GENPOOL = {
    "Ernährungstypen": ["Herbivore", "Carnivore", "Omnivore"],
    "Gene": {
        "Herbivore": {
            "Fitnesslevel": (0.8, 1.5),
            "Wahrnehmungsreichweite": (5, 10),
            # Weitere Herbivore-spezifische Gene...
        },
        "Carnivore": {
            "Fitnesslevel": (1.0, 2.0),
            "Wahrnehmungsreichweite": (6, 12),
            # Weitere Carnivore-spezifische Gene...
        },
        "Omnivore": {
            "Fitnesslevel": (0.9, 1.8),
            "Wahrnehmungsreichweite": (5, 11),
            # Weitere Omnivore-spezifische Gene...
        },
        # Weitere Ernährungstypen...
    }
}


class Lebewesen:
    def __init__(self):
        self.genetik = {}
        self.genverteilung()

    def genverteilung(self):
        # Ernährungstyp zufällig auswählen
        ernährungstyp = random.choice(GENPOOL["Ernährungstypen"])
        self.genetik["Ernährungstyp"] = ernährungstyp

        # Gene basierend auf dem Ernährungstyp verteilen
        for gen, bereich in GENPOOL["Gene"][ernährungstyp].items():
            self.genetik[gen] = round(random.uniform(*bereich), 3)

        # Zugriff auf die Gene
        self.fitnesslevel = self.genetik["Fitnesslevel"]
        self.wahrnehmungsreichweite = self.genetik["Wahrnehmungsreichweite"]



    def fortpflanzen(self, partner):
        kind = Lebewesen()
        kind.genverteilung_durch_vererbung(self, partner)
        return kind

    
    def genverteilung_durch_vererbung(self, elternteil1, elternteil2):
        for gen in GENPOOL["Gene"][self.genetik["Ernährungstyp"]]:
            gen_wert_von_elternteil1 = elternteil1.genetik[gen]
            gen_wert_von_elternteil2 = elternteil2.genetik[gen]


            # Durchschnittswert der Gene von beiden Elternteilen
            durchschnittlicher_gen_wert = (gen_wert_von_elternteil1 + gen_wert_von_elternteil2) / 2


            # Mutation hinzufügen, falls zutreffend
            if random.random() < MUTATIONS_WAHRSCHEINLICHKEIT:
                mutation = round((random.uniform(-MUTATIONS_VARIABILITÄT, MUTATIONS_VARIABILITÄT) 
                            * durchschnittlicher_gen_wert), 3)
                durchschnittlicher_gen_wert += mutation

            self.genetik[gen] = durchschnittlicher_gen_wert


# Fehlende Konstanten für die Mutation
MUTATIONS_WAHRSCHEINLICHKEIT = 0.05  # 5% Wahrscheinlichkeit
MUTATIONS_VARIABILITÄT = 0.1  # 10% Variabilität

# Erstellen von 100 Instanzen von Lebewesen
lebewesen_liste = [Lebewesen() for _ in range(100)]

if __name__ == "__main__":
    for i, lebewesen in enumerate(lebewesen_liste, start=1):
        print(f"Lebewesen {i}:")
        print(f"  Ernährungstyp: {lebewesen.genetik['Ernährungstyp']}")
        print(f"  Fitnesslevel: {lebewesen.genetik['Fitnesslevel']}")
        print(f"  Wahrnehmungsreichweite: {lebewesen.genetik['Wahrnehmungsreichweite']}\n")