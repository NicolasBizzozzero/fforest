import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.splitting_methods.split import split, SplittingMethod
from ensemble_experimentation.src.vrac import create_dir


def subsubtrain_split():
    """ Split the subtrain database into multiple subsubtrain databases. """
    number_of_trees = env.cleaned_arguments[gpn.trees_in_forest()]
    counter_size = len(str(number_of_trees))

    # Create the subsubtrain directories
    subsubtrain_names = []
    for tree_index in range(1, number_of_trees + 1):
        dir_name = env.cleaned_arguments[gpn.subsubtrain_directory_pattern()] % str(tree_index).zfill(counter_size)
        subsubtrain_names.append(dir_name)
        create_dir(env.cleaned_arguments[gpn.main_directory()] + "/" +
                   env.cleaned_arguments[gpn.subtrain_directory()] + "/" + dir_name)

    # Split the database
    row_limit = env.statistics[gsn.instances_in_subtrain()] // number_of_trees
    list_instances = \
        split(input_path=env.statistics[gsn.subtrain_path()],
              delimiter=env.cleaned_arguments[gpn.delimiter()],
              have_header=env.cleaned_arguments[gpn.have_header()],
              method=SplittingMethod.HALFING,                           # TODO: Change this
              encoding=env.cleaned_arguments[gpn.encoding()],
              class_name=env.cleaned_arguments[gpn.class_name()],
              number_of_rows=env.statistics[gsn.instances_in_subtrain()],
              tree_names=subsubtrain_names,
              subtrain_path= env.cleaned_arguments[gpn.main_directory()] + "/" + env.cleaned_arguments[gpn.subtrain_directory()],
              row_limit=row_limit)

    # Store the number of instances of each tree in the statistics file
    env.statistics[gsn.instances_in_subsubtrain()] = dict(zip(subsubtrain_names, list_instances))
