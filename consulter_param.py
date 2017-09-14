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
    parameters.impot_revenu.bareme[1].rate.update(start=reform_period.start, value=0)
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
tax_benefit_system = openfisca_france.FranceTaxBenefitSystem()

resultat_actuel = tax_benefit_system.parameters.impot_revenu.bareme[1].rate

print "Résultat actuel"
print resultat_actuel

####### Calcule la situation avec la reforme ##############
reformed_tax_benefit_system = MaReform(tax_benefit_system)

resultat_apres_reforme = reformed_tax_benefit_system.parameters.impot_revenu.bareme[1].rate

print "Resultat après reforme"
print resultat_apres_reforme
