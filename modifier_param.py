# -*- coding: utf-8 -*-

import openfisca_france
from openfisca_core.simulations import Simulation
from openfisca_core import reforms
from openfisca_core.parameters import load_parameter_file
from openfisca_core import periods

####### Décrivez votre réforme ###########
def modify_my_parameters(parameters):
    reform_year = 2017
    reform_period = periods.period(reform_year)
    parameters.impot_revenu.bareme[1].rate.update(start=reform_period, value=0)
    return parameters

class MaReform(reforms.Reform):
    def apply(self):
        self.modify_parameters(modifier_function = modify_my_parameters)



####### Décrivez les entités ###########
situation = {
  "familles": {
    "famille_1": {
      "enfants": [
        "Janet"
      ],
      "parents": [
        "Bill",
        "Bob"
      ]
    }
  },
  "foyers_fiscaux": {
    "foyer_fiscal_1": {
      "declarants": [
        "Bill",
        "Bob"
      ],
      "personnes_a_charge": [
        "Janet"
      ]
    }
  },
  "individus": {
    "Bill": {
      "salaire_de_base": {
        "2017": 20000
      }
    },
    "Bob": {
      "salaire_de_base": {
        "2017": 30000
      }
    },
    "Janet": {}
  },
  "menages": {
    "menage_1": {
      "conjoint": [
        "Bob"
      ],
      "enfants": [
        "Janet"
      ],

      "personne_de_reference": [
        "Bill"
      ]
    }
  }
}

####### Calcule la situation actuelle ##############
tax_benefit_system_actuel = openfisca_france.FranceTaxBenefitSystem()
simulation_actuelle = Simulation(tax_benefit_system=tax_benefit_system_actuel, simulation_json=situation)

resultat_actuel = simulation_actuelle.calculate('impots_directs', '2017')

print "Résultat actuel"
print resultat_actuel

####### Calcule la situation avec la reforme ##############
tax_benefit_system_reforme = MaReform(tax_benefit_system_actuel)
simulation_reforme = Simulation(tax_benefit_system=tax_benefit_system_reforme, simulation_json=situation)

resultat_reforme = simulation_reforme.calculate('impots_directs', '2017')

print "Resultat après reforme"
print resultat_reforme
