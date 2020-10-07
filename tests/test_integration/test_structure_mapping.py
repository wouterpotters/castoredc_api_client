from tests.test_integration.data_ids import form_ids, step_ids, field_ids


class TestStudyMap:
    """Tests the integration between CastorEDCClient and the CastorObjects that map the study structure."""
    def test_map_study_number(self, client):
        """Tests if the right number of forms, steps and fields are linked."""
        client.map_structure()
        assert client.study.study_id == "D234215B-D956-482D-BF17-71F2BB12A2FD"
        assert len(client.study.get_all_forms()) == len(form_ids)
        assert len(client.study.get_all_steps()) == len(step_ids)
        assert len(client.study.get_all_fields()) == len(field_ids)

    def test_map_study_ids(self, client):
        """Tests if the right ids form, step and field ids are linked."""
        client.map_structure()
        for form_id in form_ids:
            assert client.study.get_single_form(form_id) is not None
        for step_id in step_ids:
            assert client.study.get_single_step(step_id) is not None
        for field_id in field_ids:
            assert client.study.get_single_field(field_id) is not None

    def test_study_get_all_survey_forms(self, client):
        """Tests if get all survey forms returns the right forms."""
        client.map_structure()
        study = client.study
        survey_forms = study.get_all_survey_forms()
        assert len(survey_forms) == 1
        survey_form_ids = [form.form_id for form in survey_forms]
        assert "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E" in survey_form_ids

    def test_study_get_all_report_forms(self, client):
        """Tests if get all report forms returns the right forms."""
        client.map_structure()
        study = client.study
        report_forms = study.get_all_report_forms()
        assert len(report_forms) == 4
        report_form_ids = [form.form_id for form in report_forms]
        assert "89FF2394-0D41-4D4C-89FE-AA9AB287B31E" in report_form_ids
        assert "C4ADC387-9BFD-4171-A861-6B973699A6ED" in report_form_ids
        assert "770DB401-6100-4CF5-A95F-3402B55EAC48" in report_form_ids
        assert "8D4F696E-DA2E-4A0E-ACD8-2F1B71718D6E" in report_form_ids

    def test_study_form_links_model(self, client):
        """Tests if the links are in the right format."""
        client.map_structure()
        study = client.study
        study.update_links(client)
        assert len(study.form_links.keys()) == 2
        assert type(study.form_links["Report"]) is dict
        assert type(study.form_links["Survey"]) is dict

    def test_study_form_links_form(self, client):
        """Tests if the links contain the right forms."""
        client.map_structure()
        study = client.study
        study.update_links(client)
        assert "89FF2394-0D41-4D4C-89FE-AA9AB287B31E" in study.form_links["Report"]
        assert "C4ADC387-9BFD-4171-A861-6B973699A6ED" in study.form_links["Report"]
        assert "770DB401-6100-4CF5-A95F-3402B55EAC48" in study.form_links["Report"]
        assert "8D4F696E-DA2E-4A0E-ACD8-2F1B71718D6E" in study.form_links["Report"]
        assert "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E" in study.form_links["Survey"]

    def test_study_form_links_form_instances(self, client):
        """Tests if the links contain the right form instances."""
        client.map_structure()
        study = client.study
        study.update_links(client)
        # Test Reports
        assert "B68E831D-1347-4237-9F38-F79E86A58D64" in \
               study.form_links["Report"]["89FF2394-0D41-4D4C-89FE-AA9AB287B31E"]
        assert "98CB10D0-B392-4EB9-BEEF-BCBCC59D9A6F" in \
               study.form_links["Report"]["C4ADC387-9BFD-4171-A861-6B973699A6ED"]
        assert "C8EE71C5-F266-4F59-BFD3-A643643C4FE1" in \
               study.form_links["Report"]["770DB401-6100-4CF5-A95F-3402B55EAC48"]
        assert "2924E308-5718-48D6-881B-7492F350B8F7" in \
               study.form_links["Report"]["8D4F696E-DA2E-4A0E-ACD8-2F1B71718D6E"]
        # Test Surveys
        assert "QOL Survey" in \
               study.form_links["Survey"]["D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"]

    def test_map_study_data(self, client):
        """Tests if the right data is added to the objects"""
        # Test a field
        field = client.study.get_single_field("75497076-FDA2-415F-88E5-5BD51D50A8D1")
        assert field.field_id == "75497076-FDA2-415F-88E5-5BD51D50A8D1"
        assert field.field_name == "his_family"
        assert field.field_label == "Family history of disease"
        assert field.field_type == "checkbox"
        assert field.field_required is True
        assert field.field_option_group == "1D62D347-E53F-489B-B503-29BE9555428F"
        # Test a step
        step = client.study.get_single_step("AAFFB3B8-C2B6-474F-B6DC-E25B9FDE7C21")
        assert step.step_name == "Event details"
        assert step.step_id == "AAFFB3B8-C2B6-474F-B6DC-E25B9FDE7C21"
        # Test a form
        form = client.study.get_single_form("89FF2394-0D41-4D4C-89FE-AA9AB287B31E")
        assert form.form_name == "Medication"
        assert form.form_id == "89FF2394-0D41-4D4C-89FE-AA9AB287B31E"
        assert form.form_type == "Report"

    def test_map_study_link_field_step(self, client):
        """Tests if fields are linked to the right steps"""
        # Test a report field-step combination
        client.map_structure()
        assert client.study.get_single_field("F33AD264-6483-4E7F-9E1F-CF1E2655661C").step.step_id \
               == "3F7AAC2D-87CA-4C41-89A8-AB3C53472B04"
        # Test a study field-step combination
        assert client.study.get_single_field("08EA24A7-8623-4F68-A170-3A38C44F1885").step.step_id \
               == "52109C76-EB23-4BCD-95EC-10AC5CD912BF"
        # Test a survey field-step combination
        assert client.study.get_single_field("FC4FAA2D-08FD-41F7-B482-444B2B6D3116").step.step_id \
               == "C19211FE-1C53-43F9-BC85-460DF1255153"

    def test_map_study_link_step_form(self, client):
        """Tests if steps are linked to the right forms"""
        # Test a report step-form combination
        client.map_structure()
        assert client.study.get_single_step("3F7AAC2D-87CA-4C41-89A8-AB3C53472B04").form.form_id \
               == "C4ADC387-9BFD-4171-A861-6B973699A6ED"
        # Test a study step-form combination
        assert client.study.get_single_step("52109C76-EB23-4BCD-95EC-10AC5CD912BF").form.form_id \
               == "1046822E-8C8B-4D8B-B29C-183CAC8B28AF"
        # Test a survey step-form combination
        assert client.study.get_single_step("C19211FE-1C53-43F9-BC85-460DF1255153").form.form_id \
               == "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
