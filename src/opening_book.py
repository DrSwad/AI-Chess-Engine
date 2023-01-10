from typing import Dict, List, Optional


class OpeningBook:
    def __init__(self):
        self.openings = self._create_opening_book()

    def _create_opening_book(self) -> Dict[str, List[str]]:
        return {
            "Ruy Lopez": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
            "Italian Game": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
            "French Defense": ["e2e4", "e7e6"],
            "Sicilian Defense": ["e2e4", "c7c5"],
            "Caro-Kann Defense": ["e2e4", "c7c6"],
            "Scandinavian Defense": ["e2e4", "d7d5"],
            "Alekhine Defense": ["e2e4", "g8f6"],
            "Pirc Defense": ["e2e4", "d7d6", "d2d4", "g8f6"],
            "Queen's Gambit": ["d2d4", "d7d5", "c2c4"],
            "King's Indian Defense": ["d2d4", "g8f6", "c2c4", "g7g6"],
            "Nimzo-Indian Defense": ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "f8b4"],
            "English Opening": ["c2c4"],
            "Reti Opening": ["g1f3", "d7d5", "c2c4"],
            "Bird's Opening": ["f2f4"],
            "Nimzowitsch-Larsen Attack": ["b2b3"],
        }

    def get_opening_moves(self, opening_name: str) -> Optional[List[str]]:
        return self.openings.get(opening_name)

    def get_available_openings(self) -> List[str]:
        return list(self.openings.keys())
