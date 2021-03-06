#!/usr/bin/env python

"""Test form submission"""

__email__ = "nicolas.maire@unibas.ch"
__status__ = "Alpha"

from lxml import etree
import urllib2
import uuid

DEVICE_ID = "8C:77:12:5B:C1:3C"


def submit_data(data, url):
    """Submit an instance to ODKAggregate"""
    r = urllib2.Request(url, data=data, headers={'Content-Type': 'application/xml'})
    u = urllib2.urlopen(r)
    response = u.read()
    return response


def submit_from_instance_file(filename, aggregate_url):
    """Read an instance from a file and submit to ODKAggregate"""
    f = open(filename, 'r')
    data = f.read()
    f.close()
    submit_data(data, aggregate_url)


def submit_from_dict(form_dict, aggregate_url):
    """Create an instance from a dict and submit to ODKAggregate"""
    root = etree.Element('data', id=form_dict["id"])
    dev_id = etree.SubElement(root, "deviceId")
    dev_id.text = DEVICE_ID
    meta = etree.SubElement(root, "meta")
    inst_id = etree.SubElement(meta, "instanceID")
    inst_id.text = str(uuid.uuid1())
    etree.SubElement(root, "processedByMirth")
    etree.SubElement(root, "start")
    for field in form_dict["fields"]:
        if type(field[1]) == list:
            el_par = etree.SubElement(root, field[0])
            for sub_field in field[1]:
                el = etree.SubElement(el_par, sub_field[0])
                el.text = sub_field[1]
        else:
            el = etree.SubElement(root, field[0])
            el.text = field[1]
    #print(etree.tostring(root))
    submit_data(etree.tostring(root), aggregate_url)


def submit_baseline_individual(location_id, visit_id, fieldworker_id, individual_id, mother_id, father_id, first_name,
                               middle_name, last_name, gender, date_of_birth, partial_date, date_of_migration, origin,
                               reason, marital_change, end, aggregate_url):
    form_dict = {"id": "in_migration",
                 "fields": [["migrationType", "BASELINE"], ["locationId", location_id], ["visitId", visit_id],
                            ["fieldWorkerId", fieldworker_id],
                            ["individualInfo", [["individualId", individual_id], ["motherId", mother_id],
                                                ["fatherId", father_id], ["fatherId", father_id],
                                                ["firstName", first_name], ["middleName", middle_name],
                                                ["lastName", last_name], ["gender", gender],
                                                ["dateOfBirth", date_of_birth], ["partialDate", partial_date]]],
                            ["dateOfMigration", date_of_migration], ["origin", origin], ["reason", reason],
                            ["maritalChange", marital_change], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_death_registration(individual_id, field_worker_id, gender, death_within_dss, death_village,
                              have_death_certificate, visit_id, cause_of_death, date_of_death, place_of_death,
                              place_of_death_other, end, aggregate_url):
    form_dict = {"id": "death_registration",
                 "fields": [["individualId", individual_id], ["fieldWorkerId", field_worker_id], ["gender", gender],
                            ["deathWithinDSS", death_within_dss], ["deathVillage", death_village],
                            ["haveDeathCertificate", have_death_certificate], ["visitId", visit_id],
                            ["causeOfDeath", cause_of_death], ["dateOfDeath", date_of_death],
                            ["placeOfDeath", place_of_death], ["placeOfDeathOther", place_of_death_other],
                            ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_in_migration(migration_type, location_id, visit_id, fieldworker_id, individual_id,
                        date_of_migration, origin, reason, marital_change, end, aggregate_url):
    """Register an inmigration or baseline registration"""
    form_dict = {"id": "in_migration",
                 "fields": [["migrationType", migration_type], ["locationId", location_id], ["visitId", visit_id],
                            ["fieldWorkerId", fieldworker_id], ["individualId", individual_id],
                            ["dateOfMigration", date_of_migration], ["origin", origin], ["reason", reason],
                            ["maritalChange", marital_change], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_location_registration(hierarchy_id, fieldworker_id, location_id, location_name, ten_cell_leader,
                                 location_type, geopoint, end, aggregate_url):
    form_dict = {"id": "location_registration",
                 "fields": [["hierarchyId", hierarchy_id], ["fieldWorkerId", fieldworker_id],
                            ["locationId", location_id], ["locationName", location_name],
                            ["tenCellLeader", ten_cell_leader], ["locationType", location_type], ["geopoint", geopoint],
                            ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_membership(individual_id, household_id, fieldworker_id, relationship_to_group_head, start_date, end,
                      aggregate_url):
    form_dict = {"id": "membership",
                 "fields": [["individualId", individual_id], ["householdId", household_id],
                            ["fieldWorkerId", fieldworker_id], ["relationshipToGroupHead", relationship_to_group_head],
                            ["startDate", start_date], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_out_migration_registration(individual_id, fieldworker_id, visit_id, date_of_migration, name_of_destination,
                                      reason_for_out_migration, marital_change, end, aggregate_url):
    form_dict = {"id": "out_migration_registration",
                 "fields": [["individualId", individual_id], ["fieldWorkerId", fieldworker_id], ["visitId", visit_id],
                            ["dateOfMigration", date_of_migration], ["nameOfDestination", name_of_destination],
                            ["reasonForOutMigration", reason_for_out_migration], ["maritalChange", marital_change],
                            ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_pregnancy_observation(estimated_age_of_preg, preg_notes, age_of_preg_from_notes, last_period_from_notes,
                                 has_anc_clinic_visit, pregnancy_number, have_mosquito_net, slept_under_mosquito_net,
                                 treated_net, months_or_years, month_since_last_net_treatment, source_of_net,
                                 relationship_of_respondent_to_expectant, individual_id, fieldworker_id, visit_id,
                                 exptected_delivery_date, recorded_date, end, aggregate_url):
    form_dict = {"id": "pregnancy_observation",
                 "fields": [["estimatedAgeOfPreg", estimated_age_of_preg], ["pregNotes", preg_notes],
                            ["ageOfPregFromPregNotes", age_of_preg_from_notes],
                            ["lastPeriodFromPregNotes", last_period_from_notes],
                            ["hasANCClinicVisit", has_anc_clinic_visit],
                            ["pregnancyNumber", pregnancy_number], ["haveMosquitoNet", have_mosquito_net],
                            ["sleptUnderMosquitoNet", slept_under_mosquito_net], ["treatedNet", treated_net],
                            ["monthsOrYears", months_or_years],
                            ["monthsSinceLastNetTreatment", month_since_last_net_treatment],
                            ["sourceOfNet", source_of_net],
                            ["relationshipOfRespondentToExpectantMother", relationship_of_respondent_to_expectant],
                            ["individualId", individual_id], ["fieldWorkerId", fieldworker_id],
                            ["visitId", visit_id], ["expectedDeliveryDate", exptected_delivery_date],
                            ["recordedDate", recorded_date], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_pregnancy_outcome(mother_id, father_id, visit_id, fieldworker_id, nboutcomes, partial_date, birthingplace,
                             birthing_assistant, hours_or_days_in_hospital, hours_in_hospital, caesarian_or_natural,
                             total_number_children_still_living, attended_anc, number_of_attendances, recorded_date,
                             end, aggregate_url):
    form_dict = {"id": "pregnancy_outcome",
                 "fields": [["motherId", mother_id], ["fatherId", father_id], ["visitId", visit_id],
                            ["fieldWorkerId", fieldworker_id], ["nboutcomes", nboutcomes],
                            ["partialDate", partial_date], ["birthingPlace", birthingplace],
                            ["birthingAssistant", birthing_assistant],
                            ["hoursOrDaysInHospital", hours_or_days_in_hospital],
                            ["hoursInHospital", hours_in_hospital], ["caesarianOrNatural", caesarian_or_natural],
                            ["totalNumberChildrenStillLiving", total_number_children_still_living],
                            ["attendedANC", attended_anc], ["numberOfANCAttendances", number_of_attendances],
                            ["recordedDate", recorded_date], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_relationship(individual_a, individual_b, fieldworker_id, relationship_type, start_date, end, aggregate_url):
    form_dict = {"id": "relationship",
                 "fields": [["individualA", individual_a], ["individualB", individual_b],
                            ["fieldWorkerId", fieldworker_id], ["relationshipType", relationship_type],
                            ["startDate", start_date], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_social_group_registration(household_id, individual_id, field_worker_id, group_name, social_group_type, end,
                                     aggregate_url):
    form_dict = {"id": "social_group_registration", "fields": [["householdId", household_id],
                 ["individualId", individual_id], ["fieldWorkerId", field_worker_id], ["groupName", group_name],
                 ["socialGroupType", social_group_type], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)


def submit_visit_registration(visit_id, field_worker_id, location_id, round_number, visit_date, interviewee_id,
                              correct_interviewee, farmhouse, coordinates, end, aggregate_url):
    form_dict = {"id": "visit_registration",
                 "fields": [["visitId", visit_id], ["fieldWorkerId", field_worker_id], ["locationId", location_id],
                            ["roundNumber", round_number], ["visitDate", visit_date], ["intervieweeId", interviewee_id],
                            ["correctInterviewee", correct_interviewee], ["farmhouse", farmhouse],
                            ["coordinates", coordinates], ["end", end]]}
    return submit_from_dict(form_dict, aggregate_url)

