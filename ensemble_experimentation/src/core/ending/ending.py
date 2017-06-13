import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
from ensemble_experimentation.src.vrac import dump_dict


def dump_statistics_dictionary():
    dump_dict(env.statistics, env.cleaned_arguments[gpn.main_directory()] + "/" + \
              env.cleaned_arguments[gpn.statistics_file_name()])
