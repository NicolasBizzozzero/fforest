import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.vrac import create_dir
from ensemble_experimentation.src.core.splitting_methods import split


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
#    list_instances = \
#        split(filepath=env.statistics[gsn.train_path()],
        #              delimiter=env.cleaned_arguments[gpn.delimiter()],
        #     row_limit=env.cleaned_arguments[gpn.reference_value()],
        #     have_header=env.cleaned_arguments[gpn.have_header()],
        #     method=env.cleaned_arguments[gpn.reference_split_method()],
        #     output_name_train=env.statistics[gsn.reference_path()],
        #     output_name_test=env.statistics[gsn.subtrain_path()],
        #     encoding=env.cleaned_arguments[gpn.encoding()],
        #     class_name=env.cleaned_arguments[gpn.class_name()],
    #     number_of_rows=env.statistics[gsn.instances_in_train()])
    list_instances = [10 for _ in range(number_of_trees)]

    # Store the number of instances of each tree in the statistics file
    env.statistics[gsn.instances_in_subsubtrain()] = dict(zip(subsubtrain_names, list_instances))
