"""Tests for the semantic matcher implementation."""

import pytest
import torch

from src.semantic_matching.matcher import SemanticMatcher


@pytest.fixture
def matcher():
    """Create a SemanticMatcher instance for testing."""
    return SemanticMatcher(model_name="all-mpnet-base-v2", similarity_threshold=0.7)


@pytest.fixture
def sample_texts():
    """Create sample texts for testing."""
    return {
        "source_texts": ["climate change", "economic growth", "population size"],
        "target_texts": {
            "climate change": "Rise in Earth's temperature",
            "Economic growth": "Increase in economic output",
            "population size": "Study of population characteristics"
        }
    }


def test_initialization(matcher):
    """Test matcher initialization."""
    assert matcher.model_name == "all-mpnet-base-v2"
    assert matcher.similarity_threshold == 0.7
    assert isinstance(matcher.model, torch.nn.Module)
    assert matcher.device in ['cuda', 'cpu']


def test_find_matches(matcher, sample_texts):
    """Test finding matches between source and target texts."""
    matches = matcher.find_matches(
        sample_texts["source_texts"],
        sample_texts["target_texts"]
    )
    print(matches)

    # Check that matches dictionary is created
    assert isinstance(matches, dict)

    # Check that each source text has matches
    for source_text in sample_texts["source_texts"]:
        assert source_text in matches
        assert isinstance(matches[source_text], list)

        # Check that each match has the correct format [target_text, definition]
        for match in matches[source_text]:
            assert len(match) == 2
            assert match[0] in sample_texts["target_texts"]
            assert match[1] == sample_texts["target_texts"][match[0]]


def test_find_matches_empty_input(matcher):
    """Test finding matches with empty input."""
    matches = matcher.find_matches([], {})
    assert isinstance(matches, dict)
    assert len(matches) == 0


def test_find_matches_no_matches(matcher):
    """Test finding matches when no matches are found."""
    source_texts = ["unrelated text"]
    target_texts = {"different text": "definition"}

    matches = matcher.find_matches(source_texts, target_texts)
    assert isinstance(matches, dict)
    assert len(matches) == 0


def test_calculate_similarity(matcher):
    """Test calculating similarity between two texts."""
    # Test similar texts
    similarity = matcher.calculate_similarity(
        "climate change", "global warming")
    assert isinstance(similarity, float)
    assert 0 <= similarity <= 1
    assert similarity > matcher.similarity_threshold

    # Test different texts
    similarity = matcher.calculate_similarity(
        "climate change", "population size")
    assert isinstance(similarity, float)
    assert 0 <= similarity <= 1
    assert similarity < matcher.similarity_threshold


def test_calculate_similarity_same_text(matcher):
    """Test calculating similarity between identical texts."""
    similarity = matcher.calculate_similarity("test text", "test text")
    assert isinstance(similarity, float)
    assert 0 <= similarity <= 1
    assert similarity == 1.0  # Should be exactly 1 for identical texts


def test_calculate_similarity_empty_text(matcher):
    """Test calculating similarity with empty texts."""
    similarity = matcher.calculate_similarity("", "")
    assert isinstance(similarity, float)
    assert similarity != similarity  # Check if NaN

    # Test with one empty text
    similarity = matcher.calculate_similarity("test", "")
    assert isinstance(similarity, float)
    assert similarity != similarity  # Check if NaN

    similarity = matcher.calculate_similarity("", "test")
    assert isinstance(similarity, float)
    assert similarity != similarity  # Check if NaN


def test_different_threshold(matcher):
    """Test matcher with different similarity threshold."""
    # Create matcher with lower threshold
    low_threshold_matcher = SemanticMatcher(similarity_threshold=0.5)

    # Test with same texts
    source_texts = ["climate change"]
    target_texts = {"global warming": "definition"}

    # Should find more matches with lower threshold
    matches = low_threshold_matcher.find_matches(source_texts, target_texts)
    assert len(matches) > 0
    assert len(matches["climate change"]) > 0


def test_model_device(matcher):
    """Test that model is on the correct device."""
    if torch.cuda.is_available():
        assert matcher.device == 'cuda'
        assert next(matcher.model.parameters()).is_cuda
    else:
        assert matcher.device == 'cpu'
        assert not next(matcher.model.parameters()).is_cuda
