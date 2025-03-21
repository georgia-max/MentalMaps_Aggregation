
from src.core.vensim_parser import CLDParser
from pathlib import Path


def main():
    # Initialize parser
    parser = CLDParser()

    # Parse a CLD file
    variables, relationships = parser.parse(Path(
        "/Users/gl665/Documents/Phrame-MentalMaps-1/data/raw/rc_mental_models_clean/FM 51220Clean_edited.mdl"))

    # Access the results
    for var_id, var_name in variables.items():
        print(f"Variable {var_id}: {var_name}")

    for from_id, to_dict in relationships.items():
        from_name = variables[from_id]
        for to_id, attrs in to_dict.items():
            to_name = variables[to_id]
            weight = attrs['weight']
            print(f"{from_name} -> {to_name} (weight: {weight})")
    
    
    
    # # get_cld_dict() is an instance method, not a class method
    # my_dict = parser.parse()
    # print(my_dict)


if __name__ == "__main__":
    main()
