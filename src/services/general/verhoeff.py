# Esimerkki, jotta muistais myöhemmin:
# luodaan luvulle 236 tarkistusbitti
# Ensimmäisessä vaiheessa käännetää luku ja lisätää nolla -> 0632
# pysyäkseen mukana täytyy katsoa alhaalla olevaa calchecksum funktiota
# verhoeff_table_d[c][verhoeff_table_p[(i+1)%8][int(item)]]
# aluksi c ja i on kumpikin nolla eli tiedetään, että d taulun x koordinaatti on 0
# y koordinaatti saadaan p taulusta
# p taulun x koordinaatti tulee indeksi modulo 8, joka siis on 1.
# p taulun y koordinaatti on meidän käännetyn luvun ensimmäinen alkio eli 2, joten
# p(1,2) Nähdään että sen on 7 eli 7 on d taulun y koordinaatti
# Tämän avulla saadaan c muuttujan uusi arvo d(0, 7) = 7
# Seuraavassa iteraatiossa tiedetään jälleen c:n arvo 7 ja etsitään samaan tyyliin d taululle
# y:n arvo, kunnes arvo nolla tulee. Nolla laskun jälkeen katsotaan j taulusta c arvoa vastaava luku
# joka on haluttu checksum digit.


class Verhoeff:
    """Class for generating and validating Verhoeff checksums
    
    Used for generating the national SNOMED CT ids

    Tässä on lyhyt selitys siitä, miten verhoeff toimii
    luodaan luvulle 236 tarkistusbitti
    Ensimmäisessä vaiheessa käännetää luku ja lisätää nolla -> 0632
    pysyäkseen mukana täytyy katsoa alhaalla olevaa calchecksum funktiota
    verhoeff_table_d[c][verhoeff_table_p[(i+1)%8][int(item)]]
    aluksi c ja i on kumpikin nolla eli tiedetään, että d taulun x koordinaatti on 0
    y koordinaatti saadaan p taulusta
    p taulun x koordinaatti tulee indeksi modulo 8, joka siis on 1.
    p taulun y koordinaatti on meidän käännetyn luvun ensimmäinen alkio eli 2, joten
    p(1,2) Nähdään että sen on 7 eli 7 on d taulun y koordinaatti
    Tämän avulla saadaan c muuttujan uusi arvo d(0, 7) = 7
    Seuraavassa iteraatiossa tiedetään jälleen c:n arvo 7 ja etsitään samaan tyyliin d taululle
    y:n arvo, kunnes arvo nolla tulee. Nolla laskun jälkeen katsotaan j taulusta c arvoa vastaava luku
    joka on haluttu checksum digit.

    Tarkemman kuvauksen löydät täältä: https://en.wikipedia.org/wiki/Verhoeff_algorithm
    """

    def __init__(self) -> None:
        self.verhoeff_table_d = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
            (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
            (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
            (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
            (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
            (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
            (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
            (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
            (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        )

        self.verhoeff_table_p = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
            (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
            (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
            (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
            (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
            (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
            (7, 0, 4, 6, 9, 1, 3, 2, 5, 8)
        )

        self.verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def calchecksum(self, number: str) -> int:
        """Calculates the checksum digit for the given number

        Args:
            number (str): The national id number

        Returns:
            int: The checksum digit
        """

        c = 0
        for i, item in enumerate(reversed(number)):
            c = self.verhoeff_table_d[c][self.verhoeff_table_p[(
                i+1) % 8][int(item)]]
        return self.verhoeff_table_inv[c]

    def generateVerhoeff(self, number: int, partition_id: str) -> str:
        """Generates the Verhoeff checksum for the given number

        The national id consists of three parts:
        - The number which is just a running integer
        - The national code which is 1000288
        - The partition id which differentiates between terms and concepts (10=concept, 11=term)
        - The checksum digit

        Essentially we get the next available id in the national
        code space which is 1000288. Combine it with the code space
        and the partition id and calculate the checksum digit.

        Args:
            number (int): The next available fin extension id - The running index, e.g. 236
            partition_id (str): The partition id - 10 for concept, 11 for term

        Returns:
            str: The national SNOMED CT id
        """
        national_id = '1000288'
        value = f'{str(number)}{national_id}{partition_id}'
        return f'{value}{self.calchecksum(value)}'

    def validate(self, number: int) -> bool:
        """Validates the given number

        Validate based on the Verhoeff checksum.

        Args:
            number (int): A number with a Verhoeff checksum

        Returns:
            bool: True if the number is valid, False otherwise
        """
        
        c = 0
        for i, item in enumerate(reversed(str(number))):
            c = self.verhoeff_table_d[c][self.verhoeff_table_p[i % 8][int(
                item)]]
        return c == 0
    