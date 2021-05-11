import pytest

from carbonserver.database.schemas import EmissionCreate, Emission as SchemaEmission
from carbonserver.database.models import Emissions as ModelEmission

from carbonserver.api.infra.repositories.repository_emissions import InMemoryRepository


@pytest.fixture()
def emissions_repository():
    repo = InMemoryRepository()
    return repo


@pytest.fixture()
def emission_fixture() -> EmissionCreate:
    emission = EmissionCreate.parse_obj(
        {
            "timestamp": "2021-04-04T08:43:00+02:00",
            "experiment_id": "40088f1a-d28e-4980-8d80-bf5600056a14",
            "duration": 98745,
            "emissions": 1.548444,
            "energy_consumed": 57.21874,
            "country_name": "France",
            "country_iso_code": "FRA",
            "region": "france",
            "on_cloud": True,
            "cloud_provider": "aws",
            "cloud_region": "eu-west-1a",
        }
    )
    return emission


@pytest.fixture()
def model_emission() -> ModelEmission:
    model_emission = ModelEmission(
        **{
            "id": 1,
            "timestamp": "2021-04-04T08:43:00+02:00",
            "experiment_id": "40088f1a-d28e-4980-8d80-bf5600056a14",
            "duration": 98745,
            "emissions": 1.548444,
            "energy_consumed": 57.21874,
            "country_name": "France",
            "country_iso_code": "FRA",
            "region": "france",
            "on_cloud": True,
            "cloud_provider": "aws",
            "cloud_region": "eu-west-1a",
        }
    )
    return model_emission


def test_emissions_repository_saves_correct_emission(
    emissions_repository, model_emission
):
    emission = EmissionCreate.parse_obj(
        {
            "timestamp": "2021-04-04T08:43:00+02:00",
            "experiment_id": "40088f1a-d28e-4980-8d80-bf5600056a14",
            "duration": 98745,
            "emissions": 1.548444,
            "energy_consumed": 57.21874,
            "country_name": "France",
            "country_iso_code": "FRA",
            "region": "france",
            "on_cloud": True,
            "cloud_provider": "aws",
            "cloud_region": "eu-west-1a",
        }
    )
    emissions_repository.add_save_emission(emission)
    saved_emissions = emissions_repository.emissions

    assert len(saved_emissions) == 1
    assert saved_emissions[0].id == model_emission.id


def test_emissions_repository_get_db_to_class_returns_correct_object_type(
    emissions_repository, model_emission
):
    expected_schema_emission = SchemaEmission.parse_obj(
        {
            "id": 1,
            "timestamp": "2021-04-04T08:43:00+02:00",
            "experiment_id": "40088f1a-d28e-4980-8d80-bf5600056a14",
            "duration": 98745,
            "emissions": 1.548444,
            "energy_consumed": 57.21874,
            "country_name": "France",
            "country_iso_code": "FRA",
            "region": "france",
            "on_cloud": True,
            "cloud_provider": "aws",
            "cloud_region": "eu-west-1a",
        }
    )

    actual_schema_emission = emissions_repository.get_db_to_class(model_emission)

    assert expected_schema_emission == actual_schema_emission


def test_get_one_emission_returns_the_correct_emission_from_emission_id(
    emissions_repository, emission_fixture
):
    emission_id = 1
    expected_emission = SchemaEmission.parse_obj(
        {
            "id": 1,
            "timestamp": "2021-04-04T08:43:00+02:00",
            "experiment_id": "40088f1a-d28e-4980-8d80-bf5600056a14",
            "duration": 98745,
            "emissions": 1.548444,
            "energy_consumed": 57.21874,
            "country_name": "France",
            "country_iso_code": "FRA",
            "region": "france",
            "on_cloud": True,
            "cloud_provider": "aws",
            "cloud_region": "eu-west-1a",
        }
    )
    emissions_repository.add_save_emission(emission_fixture)

    actual_emission = emissions_repository.get_one_emission(emission_id)

    assert expected_emission == actual_emission


def test_get_one_emission_returns_the_correct_emission_list_from_experiment_id(
    emissions_repository, emission_fixture
):
    experiment_id = "40088f1a-d28e-4980-8d80-bf5600056a14"
    expected_emissions = [
        SchemaEmission.parse_obj(
            {
                "id": 1,
                "timestamp": "2021-04-04T08:43:00+02:00",
                "experiment_id": "40088f1a-d28e-4980-8d80-bf5600056a14",
                "duration": 98745,
                "emissions": 1.548444,
                "energy_consumed": 57.21874,
                "country_name": "France",
                "country_iso_code": "FRA",
                "region": "france",
                "on_cloud": True,
                "cloud_provider": "aws",
                "cloud_region": "eu-west-1a",
            }
        )
    ]
    emissions_repository.add_save_emission(emission_fixture)

    actual_emissions = emissions_repository.get_emissions_from_experiment(experiment_id)

    assert expected_emissions == actual_emissions
