"""Semantic matching implementation using sentence transformers."""

from typing import Dict, List, Optional

import torch
from sentence_transformers import SentenceTransformer


class SemanticMatcher:
    """Handles semantic matching between text using sentence transformers."""

    def __init__(self, model_name: str = "all-mpnet-base-v2", similarity_threshold: float = 0.7):
        """
        Initialize the semantic matcher.

        Args:
            model_name: Name of the sentence transformer model to use
            similarity_threshold: Minimum similarity score to consider a match
        """
        self.model_name = model_name
        self.similarity_threshold = similarity_threshold
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self._initialize_model()

    def _initialize_model(self) -> SentenceTransformer:
        """Initialize the sentence transformer model."""
        model = SentenceTransformer(self.model_name)
        if self.device == "cuda":
            model = model.to(self.device)
        return model

    def find_matches(self,
                     source_texts: List[str],
                     target_texts: Dict[str, str]) -> Dict[str, List[List[str]]]:
        """
        Find semantic matches between source texts and target texts.

        Args:
            source_texts: List of texts to match (e.g., CLD node names)
            target_texts: Dictionary mapping target texts to their definitions
                (e.g., variable names to their definitions)
                
            E.g. 
            source_texts: ["climate change", "economic growth", "population size"]
            target_texts: {
                "climate change": "Rise in Earth's temperature",
                "Economic growth": "Increase in economic output",
                "population size": "Study of population characteristics"
            }

        Returns:
            Dictionary mapping each source text to a list of matching target texts and their definitions:
            {
                source_text: [[matching_target, definition], 
                ....
            }
        """
        
    # TODO: I DONT KNOW, I AM SO CONFUSED. WHAT SHOULD I DO WITH MY LIFE
        # Get embeddings for source and target texts
        embeddings_source = self.model.encode(
            source_texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            device=self.device
        )

        target_texts_list = list(target_texts.keys())
        embeddings_target = self.model.encode(
            target_texts_list,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            device=self.device
        )

        # Calculate similarities
        similarities = self.model.similarity(
            embeddings_source, embeddings_target)

        # Find matches above threshold
        matches_dict = {}
        for idx_i, source_text in enumerate(source_texts):
            matches = []
            for idx_j, target_text in enumerate(target_texts_list):
                if similarities[idx_i][idx_j] > self.similarity_threshold:
                    matches.append([target_text, target_texts[target_text]])
            if matches:
                matches_dict[source_text] = matches

        return matches_dict

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.

        Args:
            text1: First text to compare
            text2: Second text to compare

        Returns:
            Similarity score between 0 and 1, or NaN if either text is empty
        """
        if not text1 or not text2:
            return float('nan')
            
        embeddings = self.model.encode(
            [text1, text2],
            batch_size=2,
            show_progress_bar=False,
            convert_to_numpy=True,
            device=self.device
        )
        return float(self.model.similarity(embeddings[0], embeddings[1]))
