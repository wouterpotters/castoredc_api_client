class TestDataStructureMap:
    """Tests the integration between CastorEDCClient and the CastorObjects that map the study structure and data."""

    def test_form_instances(self, client):
        client.map_data()
        # Report
        assert (
            client.study.get_single_form_instance(
                "D8DEFEE4-719C-49BB-BC0E-A7F04A874CFA"
            ).instance_of.form_id
            == "89FF2394-0D41-4D4C-89FE-AA9AB287B31E"
        )
        # Survey
        assert (
            client.study.get_single_form_instance(
                "33C96866-D519-4A43-826D-4D10EFAFC007"
            ).instance_of.form_id
            == "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
        )
        # Study
        assert (
            client.study.get_single_form_instance(
                "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-000007"
            ).instance_of.form_id
            == "1046822E-8C8B-4D8B-B29C-183CAC8B28AF"
        )

    def test_data_points_exist(self, client):
        client.map_data()
        # Report
        assert (
            client.study.get_single_data_point(
                "BED5EDC7-C59D-4C87-8A40-7CB353182A7E",
                "CB6EEC80-AC7C-4A2E-9D67-3E1498A898CA",
            ).instance_of.field_id
            == "BED5EDC7-C59D-4C87-8A40-7CB353182A7E"
        )
        # Survey
        assert (
            client.study.get_single_data_point(
                "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
                "6530D4AB-4705-4864-92AE-B0EC6200E8E5",
            ).instance_of.field_id
            == "ED12B07E-EDA8-4D64-8268-BE751BD5DB36"
        )
        # Study
        assert (
            client.study.get_single_data_point(
                "1D1E9B0D-91B0-4175-8DD5-30D92F05EF67",
                "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-000007",
            ).instance_of.field_id
            == "1D1E9B0D-91B0-4175-8DD5-30D92F05EF67"
        )
