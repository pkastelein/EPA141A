from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
)
from ema_workbench.em_framework.optimization import EpsilonProgress
from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns


def run_optimization(nfe=200, epsilion = 1):  # ✅ Add this function
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    if epsilion == 1:
        epsilons = [1e3] * len(model.outcomes)

    reference_values = {
        "Bmax": 175,
        "Brate": 1.5,
        "pfail": 0.5,
        "discount rate 0": 3.5,
        "discount rate 1": 3.5,
        "discount rate 2": 3.5,
        "ID flood wave shape": 4,
    }
    scen1 = {}

    for key in model.uncertainties:
        name_split = key.name.split("_")
        if len(name_split) == 1:
            scen1.update({key.name: reference_values[key.name]})
        else:
            scen1.update({key.name: reference_values[name_split[1]]})

    ref_scenario = Scenario("reference", **scen1)
    convergence_metrics = [EpsilonProgress()]
    

    with MultiprocessingEvaluator(model) as evaluator:
        results, convergence = evaluator.optimize(
            nfe=nfe,
            searchover="levers",
            epsilons=epsilons,
            convergence=convergence_metrics,
            reference=ref_scenario,
        )
    return results, convergence


    from ema_workbench.analysis import parcoords

    #outcomes = results.loc[:,
    #           ['Expected Annual Damage', 'Dike Investment Costs', 'RfR Investment Costs', 'Evacuation Costs',
     #           'Expected Number of Deaths']]
    #limits = parcoords.get_limits(outcomes)
    #axes = parcoords.ParallelAxes(limits)
    #axes.plot(outcomes)
    # we invert this axis so direction of desirability is the same
    #plt.show()


   # fig, ax1 = plt.subplots(ncols=1)
    #ax1.plot(convergence.epsilon_progress)
    #ax1.set_xlabel("nr. of generations")
    #ax1.set_ylabel(r"$\epsilon$ progress")
    #sns.despine()
    #plt.show()



# ✅ Optional: allow standalone execution
if __name__ == "__main__":
    run_optimization()
