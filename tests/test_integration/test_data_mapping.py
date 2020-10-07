class TestDataMap:
    """Tests the integration between CastorEDCClient and the CastorObjects that map the study data."""

    def test_records_exist(self, client):
        client.map_data()
        record_ids = [record.record_id for record in client.study.records]
        # Record with leading zeroes
        assert "000001" in record_ids
        # Archived record
        assert "ARCHIVED-110003" in record_ids
        # Normal record
        assert "110009" in record_ids

    def test_form_instances_exist(self, client):
        client.map_data()
        # Report
        assert (
            client.study.get_single_form_instance(
                "D8DEFEE4-719C-49BB-BC0E-A7F04A874CFA"
            )
            is not None
        )
        # Survey
        assert (
            client.study.get_single_form_instance(
                "33C96866-D519-4A43-826D-4D10EFAFC007"
            )
            is not None
        )
        # Study
        assert (
            client.study.get_single_form_instance(
                "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-000007"
            )
            is not None
        )

    def test_data_points_exist(self, client):
        client.map_data()
        # Report
        assert (
            client.study.get_single_data_point(
                "BED5EDC7-C59D-4C87-8A40-7CB353182A7E",
                "CB6EEC80-AC7C-4A2E-9D67-3E1498A898CA",
            )
            is not None
        )
        # Survey
        assert (
            client.study.get_single_data_point(
                "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
                "6530D4AB-4705-4864-92AE-B0EC6200E8E5",
            )
            is not None
        )
        # Study
        assert (
            client.study.get_single_data_point(
                "1D1E9B0D-91B0-4175-8DD5-30D92F05EF67",
                "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-000007",
            )
            is not None
        )

    def test_record_instance_link(self, client):
        client.map_data()
        # Report
        assert (
            client.study.get_single_form_instance(
                "D8DEFEE4-719C-49BB-BC0E-A7F04A874CFA"
            ).record.record_id
            == "110012"
        )
        # Survey
        assert (
            client.study.get_single_form_instance(
                "33C96866-D519-4A43-826D-4D10EFAFC007"
            ).record.record_id
            == "110006"
        )
        # Study
        assert (
            client.study.get_single_form_instance(
                "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-110012"
            ).record.record_id
            == "110012"
        )

    def test_instance_data_point_link(self, client):
        client.map_data()
        # Report
        data_point = client.study.get_single_data_point(
            "BED5EDC7-C59D-4C87-8A40-7CB353182A7E",
            "CB6EEC80-AC7C-4A2E-9D67-3E1498A898CA",
        )
        assert (
            data_point.form_instance.instance_id
            == "CB6EEC80-AC7C-4A2E-9D67-3E1498A898CA"
        )
        assert data_point.form_instance.record.record_id == "110001"
        # Survey
        data_point = client.study.get_single_data_point(
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "6530D4AB-4705-4864-92AE-B0EC6200E8E5",
        )
        assert (
            data_point.form_instance.instance_id
            == "6530D4AB-4705-4864-92AE-B0EC6200E8E5"
        )
        assert data_point.form_instance.record.record_id == "000001"

        # Study
        data_point = client.study.get_single_data_point(
            "1D1E9B0D-91B0-4175-8DD5-30D92F05EF67",
            "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-000007",
        )
        assert (
            data_point.form_instance.instance_id
            == "1046822E-8C8B-4D8B-B29C-183CAC8B28AF-000007"
        )
        assert data_point.form_instance.record.record_id == "000007"
