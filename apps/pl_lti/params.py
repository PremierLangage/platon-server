#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  params.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

import dataclasses
from typing import Optional, Any


context_id = "context_id"
context_label = "context_label"
context_title = "context_title"
context_type = "context_type"
custom_lineitem_url = "custom_lineitem_url"
custom_lineitems_url = "custom_lineitems_url"
ext_lms = "ext_lms"
ext_user_username = "ext_user_username"
launch_presentation_document_target = "launch_presentation_document_target"
launch_presentation_locale = "launch_presentation_locale"
launch_presentation_return_url = "launch_presentation_return_url"
lis_course_section_sourcedid = "lis_course_section_sourcedid"
lis_outcome_service_url = "lis_outcome_service_url"
lis_person_contact_email_primary = "lis_person_contact_email_primary"
lis_person_name_family = "lis_person_name_family"
lis_person_name_full = "lis_person_name_full"
lis_person_name_given = "lis_person_name_given"
lis_person_sourcedid = "lis_person_sourcedid"
lis_result_sourcedid = "lis_result_sourcedid"
lti_message_type = "lti_message_type"
lti_version = "lti_version"
oauth_callback = "oauth_callback"
oauth_consumer_key = "oauth_consumer_key"
oauth_nonce = "oauth_nonce"
oauth_signature = "oauth_signature"
oauth_signature_method = "oauth_signature_method"
oauth_timestamp = "oauth_timestamp"
oauth_version = "oauth_version"
resource_link_description = "resource_link_description"
resource_link_id = "resource_link_id"
resource_link_title = "resource_link_title"
roles = "roles"
tool_consumer_info_product_family_code = "tool_consumer_info_product_family_code"
tool_consumer_info_version = "tool_consumer_info_version"
tool_consumer_instance_contact_email = "tool_consumer_instance_contact_email"
tool_consumer_instance_description = "tool_consumer_instance_description"
tool_consumer_instance_guid = "tool_consumer_instance_guid"
tool_consumer_instance_name = "tool_consumer_instance_name"
tool_consumer_instance_url = "tool_consumer_instance_url"
user_id = "user_id"
user_image = "user_image"

LTI_MANDATORY = [
    lti_message_type,
    lti_version,
    resource_link_id,
    oauth_consumer_key,
    oauth_signature_method,
    oauth_timestamp,
    oauth_nonce,
    oauth_signature,

    context_id,
    context_title,
    user_id,
    tool_consumer_instance_guid,
    tool_consumer_instance_description,
    launch_presentation_locale,
    lis_person_contact_email_primary,
    lis_person_name_family,
    lis_person_name_given,
    roles,
]



@dataclasses.dataclass
class LTIParams:
    """Representation of a LTI request params.
    https://www.imsglobal.org/specs/ltiv1p0/implementation-guide
    """

    context_id: Optional[str] = None
    context_label: Optional[str] = None
    context_title: Optional[str] = None
    context_type: Optional[str] = None
    custom_lineitem_url: Optional[str] = None
    custom_lineitems_url: Optional[str] = None
    ext_lms: Optional[str] = None
    ext_user_username: Optional[str] = None
    launch_presentation_document_target: Optional[str] = None
    launch_presentation_locale: Optional[str] = None
    launch_presentation_return_url: Optional[str] = None
    lis_course_section_sourcedid: Optional[str] = None
    lis_outcome_service_url: Optional[str] = None
    lis_person_contact_email_primary: Optional[str] = None
    lis_person_name_family: Optional[str] = None
    lis_person_name_full: Optional[str] = None
    lis_person_name_given: Optional[str] = None
    lis_person_sourcedid: Optional[str] = None
    lis_result_sourcedid: Optional[str] = None
    lti_message_type: Optional[str] = None
    lti_version: Optional[str] = None
    oauth_callback: Optional[str] = None
    oauth_consumer_key: Optional[str] = None
    oauth_nonce: Optional[str] = None
    oauth_signature: Optional[str] = None
    oauth_signature_method: Optional[str] = None
    oauth_timestamp: Optional[str] = None
    oauth_version: Optional[str] = None
    resource_link_description: Optional[str] = None
    resource_link_id: Optional[str] = None
    resource_link_title: Optional[str] = None
    roles: Optional[str] = None
    tool_consumer_info_product_family_code: Optional[str] = None
    tool_consumer_info_version: Optional[str] = None
    tool_consumer_instance_contact_email: Optional[str] = None
    tool_consumer_instance_description: Optional[str] = None
    tool_consumer_instance_guid: Optional[str] = None
    tool_consumer_instance_name: Optional[str] = None
    tool_consumer_instance_url: Optional[str] = None
    user_id: Optional[str] = None
    user_image: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LTIParams':
        assert isinstance(obj, dict)
        for e in LTI_MANDATORY:
            v = obj.get(e)
            if v is None:
                raise AssertionError(f"LTI: Missing mandatory param '{e}'")
            if not v.strip():
                raise AssertionError(f"LTI: Missing mandatory param '{e}'")
        
        return LTIParams(
            context_id=obj.get(context_id, ""),
            context_label=obj.get(context_label, ""),
            context_title=obj.get(context_title, ""),
            context_type=obj.get(context_type, ""),
            custom_lineitem_url=obj.get(custom_lineitem_url, ""),
            custom_lineitems_url=obj.get(custom_lineitems_url, ""),
            ext_lms=obj.get(ext_lms, ""),
            ext_user_username=obj.get(ext_user_username, ""),
            launch_presentation_document_target=obj.get(launch_presentation_document_target, ""),
            launch_presentation_locale=obj.get(launch_presentation_locale, ""),
            launch_presentation_return_url=obj.get(launch_presentation_return_url, ""),
            lis_course_section_sourcedid=obj.get(lis_course_section_sourcedid, ""),
            lis_outcome_service_url=obj.get(lis_outcome_service_url, ""),
            lis_person_contact_email_primary=obj.get(lis_person_contact_email_primary, ""),
            lis_person_name_family=obj.get(lis_person_name_family, ""),
            lis_person_name_full=obj.get(lis_person_name_full, ""),
            lis_person_name_given=obj.get(lis_person_name_given, ""),
            lis_person_sourcedid=obj.get(lis_person_sourcedid, ""),
            lis_result_sourcedid=obj.get(lis_result_sourcedid, ""),
            lti_message_type=obj.get(lti_message_type, ""),
            lti_version=obj.get(lti_version, ""),
            oauth_callback=obj.get(oauth_callback, ""),
            oauth_consumer_key=obj.get(oauth_consumer_key, ""),
            oauth_nonce=obj.get(oauth_nonce, ""),
            oauth_signature=obj.get(oauth_signature, ""),
            oauth_signature_method=obj.get(oauth_signature_method, ""),
            oauth_timestamp=obj.get(oauth_timestamp, ""),
            oauth_version=obj.get(oauth_version, ""),
            resource_link_description=obj.get(resource_link_description, ""),
            resource_link_id=obj.get(resource_link_id, ""),
            resource_link_title=obj.get(resource_link_title, ""),
            roles=obj.get(roles, ""),
            tool_consumer_info_product_family_code=obj.get(tool_consumer_info_product_family_code, ""),
            tool_consumer_info_version=obj.get(tool_consumer_info_version, ""),
            tool_consumer_instance_contact_email=obj.get(tool_consumer_instance_contact_email, ""),
            tool_consumer_instance_description=obj.get(tool_consumer_instance_description, ""),
            tool_consumer_instance_guid=obj.get(tool_consumer_instance_guid, ""),
            tool_consumer_instance_name=obj.get(tool_consumer_instance_name, ""),
            tool_consumer_instance_url=obj.get(tool_consumer_instance_url, ""),
            user_id=obj.get(user_id, ""),
            user_image=obj.get(user_image, ""),
        )


    def clone(self):
        return LTIParams.from_dict(self.to_dict())


    def to_dict(self):
        return dataclasses.asdict(self)
