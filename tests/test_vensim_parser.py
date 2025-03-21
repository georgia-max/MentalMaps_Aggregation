from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.parsers.vensim_parser import CLDParser, VensimLink, VensimNode, VensimParser

@pytest.fixture
def sample_vensim_file():
    """Use a real Vensim file from the test data directory"""
    base_dir = Path(__file__).parent
    print(base_dir)
    
    file_path = base_dir / "test_data" / "test_model.mdl"
    if not file_path.exists():
        pytest.skip("Real Vensim test file not found")
    
    
    return file_path

@pytest.fixture
def sample_vensim_file_alt(tmp_path):
    """Create a sample Vensim file with alternative end pattern"""
    content = """Some header
*View 1
10,1,Variable1,"Stock Variable"
10,2,Variable2,"Flow Variable"
1,1,1,2,0,0,43
1,2,2,1,0,0,45
///---\\
"""
    file_path = tmp_path / "test_alt.mdl"
    with open(file_path, 'w') as f:
        f.write(content)
    return file_path


@pytest.fixture
def parser():
    return VensimParser()


@pytest.fixture
def cld_parser():
    return CLDParser()


def test_read_file(parser, sample_vensim_file):
    """Test reading a Vensim file"""
    df = parser.read_file(sample_vensim_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4  # 2 variables + 2 links
    assert all(col in df.columns for col in [0, 1, 2, 3, 6])


def test_read_file_alt_end_pattern(parser, sample_vensim_file_alt):
    """Test reading a Vensim file with alternative end pattern"""
    df = parser.read_file(sample_vensim_file_alt)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4


def test_read_file_nonexistent(parser):
    """Test reading a nonexistent file"""
    with pytest.raises(FileNotFoundError):
        parser.read_file(Path("nonexistent.mdl"))


def test_extract_content(parser, sample_vensim_file):
    """Test content extraction from file"""
    with open(sample_vensim_file, 'r') as f:
        lines = f.readlines()
    content = parser._extract_content(lines)
    assert len(content) == 4  # 2 variables + 2 links
    assert all(',' in line for line in content)


def test_create_dataframe(parser):
    """Test DataFrame creation from content"""
    content = [
        "10,1,Variable1,Stock Variable",
        "1,1,1,2,0,0,43"
    ]
    df = parser._create_dataframe(content)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df[0].dtype == np.int64


def test_cld_parser_parse(cld_parser, sample_vensim_file):
    """Test CLD parser's parse method"""
    variables, relationships = cld_parser.parse(sample_vensim_file)

    # Test variables
    assert isinstance(variables, dict)
    assert len(variables) == 2
    assert all(isinstance(v, str) for v in variables.values())

    # Test relationships
    assert isinstance(relationships, dict)
    assert len(relationships) == 2
    assert all(isinstance(rel, dict) for rel in relationships.values())


def test_extract_variables(cld_parser, sample_vensim_file):
    """Test variable extraction"""
    df = cld_parser.read_file(sample_vensim_file)
    variables = cld_parser._extract_variables(df)

    assert isinstance(variables, dict)
    assert len(variables) == 2
    assert all(isinstance(v, str) for v in variables.values())
    assert all('"' not in v for v in variables.values())  # No quotes in names


def test_clean_variable_name(cld_parser):
    """Test variable name cleaning"""
    test_cases = [
        ('"Variable1"', 'variable1'),
        ('Variable2 ', 'variable2'),
        ('"Variable3" ', 'variable3')
    ]

    for input_name, expected in test_cases:
        assert cld_parser._clean_variable_name(input_name) == expected


def test_extract_relationships(cld_parser, sample_vensim_file):
    """Test relationship extraction"""
    df = cld_parser.read_file(sample_vensim_file)
    relationships = cld_parser._extract_relationships(df)

    assert isinstance(relationships, dict)
    assert len(relationships) == 2
    assert all(isinstance(rel, dict) for rel in relationships.values())
    assert all('weight' in rel for rels in relationships.values()
               for rel in rels.values())


def test_prepare_links_dataframe(cld_parser, sample_vensim_file):
    """Test links DataFrame preparation"""
    df = cld_parser.read_file(sample_vensim_file)
    df_links = cld_parser._prepare_links_dataframe(df)

    assert isinstance(df_links, pd.DataFrame)
    assert all(col in df_links.columns for col in [
               'type', 'index', 'from', 'to', 'polarity', 'weight'])
    assert df_links['weight'].dtype in [np.int64, np.float64]


def test_create_relationships_dict(cld_parser):
    """Test relationships dictionary creation"""
    df_links = pd.DataFrame({
        'from': [1, 2],
        'to': [2, 1],
        'weight': [1, -1]
    })

    relationships = cld_parser._create_relationships_dict(df_links)

    assert isinstance(relationships, dict)
    assert len(relationships) == 2
    assert relationships[1][2]['weight'] == 1
    assert relationships[2][1]['weight'] == -1


def test_get_json_cld(cld_parser, sample_vensim_file):
    """Test JSON CLD generation"""
    cld_data = cld_parser.get_json_cld()

    assert isinstance(cld_data, dict)
    assert 'variables' in cld_data
    assert 'relationships' in cld_data
    assert isinstance(cld_data['variables'], dict)
    assert isinstance(cld_data['relationships'], dict)
