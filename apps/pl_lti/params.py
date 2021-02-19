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


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception:
            pass
    assert False


def read_str(obj: Any, name: str) -> str:
    o = obj.get(name)
    if type(o) is str:
        return o

    return from_union(
        [from_none, lambda x: from_str(x)],
        obj.get(name)
    )


def read_int(obj: Any, name: str) -> str:
    o = obj.get(name)
    if type(o) is int:
        return o

    return from_union(
        [from_none, lambda x: int(from_str(x))],
        obj.get(name)
    )


@dataclasses.dataclass
class LTIParams:
    """Representation of a LTI request params.
    https://www.imsglobal.org/specs/ltiv1p0/implementation-guide
    """

    oauth_timestamp: Optional[int] = None
    user_id: Optional[int] = None
    user_image: Optional[str] = None
    lis_person_sourcedid: Optional[int] = None
    context_id: Optional[int] = None
    resource_link_id: Optional[int] = None
    oauth_version: Optional[str] = None
    oauth_nonce: Optional[str] = None
    oauth_consumer_key: Optional[str] = None
    roles: Optional[str] = None
    context_label: Optional[str] = None
    context_title: Optional[str] = None
    resource_link_title: Optional[str] = None
    resource_link_description: Optional[str] = None
    context_type: Optional[str] = None
    lis_course_section_sourcedid: Optional[str] = None
    lis_result_sourcedid: Optional[str] = None
    lis_outcome_service_url: Optional[str] = None
    lis_person_name_given: Optional[str] = None
    lis_person_name_family: Optional[str] = None
    lis_person_name_full: Optional[str] = None
    ext_user_username: Optional[str] = None
    lis_person_contact_email_primary: Optional[str] = None
    launch_presentation_locale: Optional[str] = None
    ext_lms: Optional[str] = None
    tool_consumer_info_product_family_code: Optional[str] = None
    tool_consumer_info_version: Optional[str] = None
    oauth_callback: Optional[str] = None
    lti_version: Optional[str] = None
    lti_message_type: Optional[str] = None
    tool_consumer_instance_guid: Optional[str] = None
    tool_consumer_instance_name: Optional[str] = None
    tool_consumer_instance_description: Optional[str] = None
    launch_presentation_document_target: Optional[str] = None
    launch_presentation_return_url: Optional[str] = None
    custom_lineitems_url: Optional[str] = None
    custom_lineitem_url: Optional[str] = None
    oauth_signature_method: Optional[str] = None
    oauth_signature: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LTIParams':
        assert isinstance(obj, dict)
        return LTIParams(
            oauth_timestamp=read_int(obj, "oauth_timestamp"),
            user_id=read_int(obj, "user_id"),
            user_image=read_str(obj, "user_image"),
            lis_person_sourcedid=read_int(obj, "lis_person_sourcedid"),
            context_id=read_int(obj, "context_id"),
            resource_link_id=read_int(obj, "resource_link_id"),
            oauth_version=read_str(obj, "oauth_version"),
            oauth_nonce=read_str(obj, "oauth_nonce"),
            oauth_consumer_key=read_str(obj, "oauth_consumer_key"),
            roles=read_str(obj, "roles"),
            context_label=read_str(obj, "context_label"),
            context_title=read_str(obj, "context_title"),
            resource_link_title=read_str(obj, "resource_link_title"),
            resource_link_description=read_str(obj, "resource_link_description"),
            context_type=read_str(obj, "context_type"),
            lis_course_section_sourcedid=read_str(obj, "lis_course_section_sourcedid"),
            lis_result_sourcedid=read_str(obj, "lis_result_sourcedid"),
            lis_outcome_service_url=read_str(obj, "lis_outcome_service_url"),
            lis_person_name_given=read_str(obj, "lis_person_name_given"),
            lis_person_name_family=read_str(obj, "lis_person_name_family"),
            lis_person_name_full=read_str(obj, "lis_person_name_full"),
            ext_user_username=read_str(obj, "ext_user_username"),
            lis_person_contact_email_primary=read_str(obj, "lis_person_contact_email_primary"),
            launch_presentation_locale=read_str(obj, "launch_presentation_locale"),
            ext_lms=read_str(obj, "ext_lms"),
            tool_consumer_info_product_family_code=read_str(obj, "tool_consumer_info_product_family_code"),
            tool_consumer_info_version=read_str(obj, "tool_consumer_info_version"),
            oauth_callback=read_str(obj, "oauth_callback"),
            lti_version=read_str(obj, "lti_version"),
            lti_message_type=read_str(obj, "oauth_tilti_message_typemestamp"),
            tool_consumer_instance_guid=read_str(obj, "tool_consumer_instance_guid"),
            tool_consumer_instance_name=read_str(obj, "tool_consumer_instance_name"),
            tool_consumer_instance_description=read_str(obj, "tool_consumer_instance_description"),
            launch_presentation_document_target=read_str(obj, "launch_presentation_document_target"),
            launch_presentation_return_url=read_str(obj, "launch_presentation_return_url"),
            custom_lineitems_url=read_str(obj, "custom_lineitems_url"),
            custom_lineitem_url=read_str(obj, "custom_lineitem_url"),
            oauth_signature_method=read_str(obj, "oauth_signature_method"),
            oauth_signature=read_str(obj, "oauth_signature"),
        )


    def to_dict(self):
        return dataclasses.asdict(self)