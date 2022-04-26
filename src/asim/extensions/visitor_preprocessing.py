# Import Modules
import yaml

from visitor_tour_scheduling import *
from visitor_tour_enum import *
from visitor_tour_frequency import *

#   This script prepares visitor data for:
#   1. Tour enumeration generates tours with party size, income,
#   segment (Personal or Business) [calculate_n_parties()], and car availability.

# Main injection point for preprocessing
def preprocess_visitor():
    # Read the visitor settings YAML
    with open('configs/visitor/preprocessing.yaml') as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)

    # Read in the CSV-stored distribution values indicated in the yaml
    tables = load_tables(
        file_path=parameters['tables_dir'],
        nested_dict=parameters['input_data']
    )

    # Add in the land_use table from data
    tables['land_use'] = pd.read_csv(
        os.path.join(*[parameters.get(x) for x in ['data_dir', 'land_use']])
    )

    # Generate tours
    print("Generating visitor tours")

    # TODO NEED TO WRITE THESE TO CSV WITHIN EACH FUNCTION

    processed_data = create_tour_enumeration(tables, parameters)

    # Setup
    processed_data['tour_scheduling_probs'] = create_tour_scheduling_probs(tables['tour_TOD'], parameters)

    # create_stop_freq_specs(tables['stop_frequency'], parameters)

    # create/update configs in place
    ##### create_scheduling_probs_and_alts(settings, los_settings)
    # create_skims_and_tap_files(settings, new_mazs)
    # create_stop_freq_specs(settings)
    # update_trip_purpose_probs(settings)
    # create_trip_scheduling_duration_probs(settings, los_settings)


    # Save to csv
    # tour_scheduling_probs.to_csv()

    return processed_data


def load_tables(file_path, nested_dict):
    # This function recursively loads all the CSV tables from the yaml file
    # and returns a mirrored nested dict with tables where CSV file paths were stored
    output = copy.deepcopy(nested_dict)
    for k, v in output.items():
        if isinstance(v, dict):
            output[k] = load_tables(file_path, v)
        else:
            output[k] = pd.read_csv(os.path.join(file_path, v))
    return output


if __name__ == '__main__':
    # Testing
    os.chdir('src/asim')
    # os.chdir('../asim')
    data = preprocess_visitor()
    # maz = self.tables['land_use'].loc[0,]