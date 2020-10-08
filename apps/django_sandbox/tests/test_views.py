import json

import dgeq

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.test import Client, TransactionTestCase
from django.urls import reverse

from common.enums import ErrorCode
from django_sandbox.models import ContainerSpecs, Sandbox, SandboxSpecs

SANDBOX_URL = settings.SANDBOX_URL


class SandboxViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.client = Client()
        self.client.force_login(self.user)

    def test_get_single(self):
        response = self.client.get(reverse("django_sandbox:sandbox", args=(self.sandbox.pk,)))
        expected = {
            "status": True,
            "row":    dgeq.serialize(self.sandbox),
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_collection(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        Sandbox.objects.create(
            name="Dummy 2", url="http://localhost:7778", enabled=False
        )
        response = self.client.get(
            reverse("django_sandbox:sandbox_collection"), data={"enabled": "1"}
        )
        expected = {
            "status": True,
            "rows":   [
                dgeq.serialize(self.sandbox),
                dgeq.serialize(sandbox_dummy1),
            ]
        }

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_get_404(self):
        response = self.client.get(reverse("django_sandbox:sandbox", args=(9999,)))
        expected = {
            "status":  False,
            "message": "Sandbox matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_403(self):
        response = Client().get(reverse("django_sandbox:sandbox", args=(self.sandbox.pk,)))
        expected = {
            "status":  False,
            "message": "Missing view permission on Sandbox",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertEqual(expected, response.json())


    def test_post_ok(self):
        data = {
            "name":    "Dummy 1",
            "url":     "http://localhost:7777",
            "enabled": False
        }
        response = self.client.post(
            reverse("django_sandbox:sandbox_collection"), data=data,
            content_type="application/json"
        )
        expected = {
            "status": True,
            "row":    dgeq.serialize(Sandbox.objects.get(name="Dummy 1"))
        }
        self.assertEqual(201, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_post_400_invalid_json(self):
        response = self.client.post(
            reverse("django_sandbox:sandbox_collection"), data="{fhze}",
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Expecting property name enclosed in double quotes: line 1 column 2 "
                       "(char 1)",
            "code":    ErrorCode.JSONDecodeError.value
        }
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_post_400_validation_error(self):
        data = {
            "name": "Dummy 1",
            "url":  "http://localhost:7777",
        }
        response = self.client.post(
            reverse("django_sandbox:sandbox_collection"), data=data,
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "{'enabled': ['Missing field']}",
            "code":    ErrorCode.ValidationError.value
        }
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_post_403(self):
        response = Client().post(
            reverse("django_sandbox:sandbox_collection"), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Missing create permission on Sandbox",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_post_404_single(self):
        response = Client().post(
            reverse("django_sandbox:sandbox", args=(1,)), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Page not found",
            "code":    ErrorCode.Http404.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_delete(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        expected = {
            "status": True,
            "row":    dgeq.serialize(sandbox_dummy1),
        }

        response = self.client.delete(reverse("django_sandbox:sandbox", args=(sandbox_dummy1.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_delete_404_sandbox_not_found(self):
        response = self.client.delete(reverse("django_sandbox:sandbox", args=(9999,)))
        expected = {
            "status":  False,
            "message": "Sandbox matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_delete_404_collection(self):
        response = self.client.delete(reverse("django_sandbox:sandbox_collection"))
        expected = {
            "status":  False,
            "message": "Page not found",
            "code":    ErrorCode.Http404.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_delete_403(self):
        response = Client().delete(reverse("django_sandbox:sandbox", args=(1,)))
        expected = {
            "status":  False,
            "message": "Missing delete permission on Sandbox",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_patch(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        data = {"name": "Modified"}
        response = self.client.patch(
            reverse("django_sandbox:sandbox", args=(sandbox_dummy1.pk,)), data=data,
            content_type="application/json"
        )
        sandbox_dummy1.refresh_from_db()
        expected = {
            "status": True,
            "row":    dgeq.serialize(sandbox_dummy1),
        }
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, response.json())
        self.assertEqual("Modified", response.json()["row"]["name"])


    def test_patch_404_collection(self):
        response = self.client.patch(
            reverse("django_sandbox:sandbox_collection"), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Page not found",
            "code":    ErrorCode.Http404.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_patch_404_sandbox_not_found(self):
        response = self.client.patch(
            reverse("django_sandbox:sandbox", args=(9999,)), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Sandbox matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_patch_400_invalid_json(self):
        response = self.client.patch(
            reverse("django_sandbox:sandbox", args=(self.sandbox.pk,)), data="{fhze}",
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Expecting property name enclosed in double quotes: line 1 column 2 "
                       "(char 1)",
            "code":    ErrorCode.JSONDecodeError.value
        }
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_patch_400_validation_error(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        data = {"unknown": "unknown"}
        response = self.client.patch(
            reverse("django_sandbox:sandbox", args=(sandbox_dummy1.pk,)), data=data,
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "{'unknown': ['Unknown field']}",
            "code":    ErrorCode.ValidationError.value
        }
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_patch_403(self):
        response = Client().patch(
            reverse("django_sandbox:sandbox", args=(1,)), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Missing change permission on Sandbox",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_put(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        data = {
            "name":    "Modified",
            "url":     "http://localhost:7777",
            "enabled": False
        }
        response = self.client.put(
            reverse("django_sandbox:sandbox", args=(sandbox_dummy1.pk,)), data=data,
            content_type="application/json"
        )
        sandbox_dummy1.refresh_from_db()
        expected = {
            "status": True,
            "row":    dgeq.serialize(sandbox_dummy1),
        }
        self.assertDictEqual(expected, response.json())
        self.assertEqual("Modified", response.json()["row"]["name"])


    def test_put_404_collection(self):
        response = self.client.put(
            reverse("django_sandbox:sandbox_collection"), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Page not found",
            "code":    ErrorCode.Http404.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_put_404_sandbox_not_found(self):
        response = self.client.put(
            reverse("django_sandbox:sandbox", args=(9999,)), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Sandbox matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_put_400_invalid_json(self):
        response = self.client.put(
            reverse("django_sandbox:sandbox", args=(self.sandbox.pk,)), data="{fhze}",
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Expecting property name enclosed in double quotes: line 1 column 2 "
                       "(char 1)",
            "code":    ErrorCode.JSONDecodeError.value
        }
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_put_400_validation_error(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        data = {
            "name":    "Modified",
            "enabled": False
        }
        response = self.client.put(
            reverse("django_sandbox:sandbox", args=(sandbox_dummy1.pk,)), data=data,
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "{'url': ['Missing field']}",
            "code":    ErrorCode.ValidationError.value
        }
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_put_403(self):
        response = Client().put(
            reverse("django_sandbox:sandbox", args=(1,)), data={},
            content_type="application/json"
        )
        expected = {
            "status":  False,
            "message": "Missing change permission on Sandbox",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertDictEqual(expected, response.json())



class SandboxSpecsViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.specs = SandboxSpecs.objects.get(sandbox=self.sandbox)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.client = Client()
        self.client.force_login(self.user)


    def test_get_single(self):
        response = self.client.get(reverse("django_sandbox:sandbox_specs", args=(self.specs.pk,)))
        expected = {
            "status": True,
            "row":    dgeq.serialize(self.specs),
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_collection(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        Sandbox.objects.create(
            name="Dummy 2", url="http://localhost:7778", enabled=False
        )
        response = self.client.get(
            reverse("django_sandbox:sandbox_specs_collection"),
            data={"sandbox": f"]{sandbox_dummy1.pk}"}
        )
        expected = {
            "status": True,
            "rows":   [
                dgeq.serialize(self.specs),
                dgeq.serialize(SandboxSpecs.objects.get(sandbox=sandbox_dummy1)),
            ]
        }

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_get_404(self):
        response = self.client.get(reverse("django_sandbox:sandbox_specs", args=(9999,)))
        expected = {
            "status":  False,
            "message": "SandboxSpecs matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_403(self):
        response = Client().get(reverse("django_sandbox:sandbox_specs", args=(self.specs.pk,)))
        expected = {
            "status":  False,
            "message": "Missing view permission on SandboxSpecs",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertEqual(expected, response.json())



class ContainerSpecsViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.specs = ContainerSpecs.objects.get(sandbox=self.sandbox)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.client = Client()
        self.client.force_login(self.user)


    def test_get_single(self):
        response = self.client.get(reverse("django_sandbox:container_specs", args=(self.specs.pk,)))
        expected = {
            "status": True,
            "row":    dgeq.serialize(self.specs),
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_collection(self):
        sandbox_dummy1 = Sandbox.objects.create(
            name="Dummy 1", url="http://localhost:7777", enabled=True
        )
        Sandbox.objects.create(
            name="Dummy 2", url="http://localhost:7778", enabled=False
        )
        response = self.client.get(
            reverse("django_sandbox:container_specs_collection"),
            data={"sandbox": f"]{sandbox_dummy1.pk}"}
        )
        expected = {
            "status": True,
            "rows":   [
                dgeq.serialize(self.specs),
                dgeq.serialize(ContainerSpecs.objects.get(sandbox=sandbox_dummy1)),
            ]
        }

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, response.json())


    def test_get_404(self):
        response = self.client.get(reverse("django_sandbox:container_specs", args=(9999,)))
        expected = {
            "status":  False,
            "message": "ContainerSpecs matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_403(self):
        response = Client().get(reverse("django_sandbox:container_specs", args=(self.specs.pk,)))
        expected = {
            "status":  False,
            "message": "Missing view permission on ContainerSpecs",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertEqual(expected, response.json())



class UsageViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.usage = async_to_sync(self.sandbox.poll_usage)()
        self.client = Client()
        self.client.force_login(self.user)


    def test_get_single(self):
        response = self.client.get(reverse("django_sandbox:usage", args=(self.usage.pk,)))
        # Encode and decode the expected output so that the date format match
        expected = json.loads(DjangoJSONEncoder().encode({
            "status": True,
            "row":    dgeq.serialize(self.usage),
        }))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_collection(self):
        usage1 = async_to_sync(self.sandbox.poll_usage)()
        usage2 = async_to_sync(self.sandbox.poll_usage)()
        response = self.client.get(
            reverse("django_sandbox:usage_collection"), data={"id": f"[{usage1.pk}"}
        )
        # Encode and decode the expected output so that the date format match
        expected = json.loads(DjangoJSONEncoder().encode({
            "status": True,
            # Sorted by date so usage 2 will be first
            "rows":   [
                dgeq.serialize(usage2),
                dgeq.serialize(usage1),
            ]
        }))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_404(self):
        response = self.client.get(reverse("django_sandbox:usage", args=(9999,)))
        expected = {
            "status":  False,
            "message": "Usage matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_403(self):
        response = Client().get(reverse("django_sandbox:usage", args=(self.usage.pk,)))
        expected = {
            "status":  False,
            "message": "Missing view permission on Usage",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertEqual(expected, response.json())



class ResponseViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.response = async_to_sync(self.sandbox.execute)(
            self.user, {"commands": ["true"]}
        ).response
        self.client = Client()
        self.client.force_login(self.user)

    """ TODO
    def test_get_single(self):
        response = self.client.get(
            reverse("django_sandbox:response", args=(self.response.pk,))
        )
        expected = {
            "status": True,
            "row":    dgeq.serialize(self.response),
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
    """
    """ TODO
    def test_get_collection(self):
        response1 = async_to_sync(self.sandbox.execute)(
            self.user, {"commands": ["true"]}
        ).response
        response2 = async_to_sync(
            self.sandbox.execute)(self.user, {"commands": ["true"]}
        ).response
        response = self.client.get(
            reverse("django_sandbox:response_collection"),
            data={"id": f"[{response1.pk}"}
        )
        expected = {
            "status": True,
            "rows":   [
                dgeq.serialize(response1),
                dgeq.serialize(response2),
            ]
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
    """

    def test_get_404(self):
        response = self.client.get(reverse("django_sandbox:response", args=(9999,)))
        expected = {
            "status":  False,
            "message": "Response matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_403(self):
        response = Client().get(reverse("django_sandbox:response", args=(self.response.pk,)))
        expected = {
            "status":  False,
            "message": "Missing view permission on Response",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertEqual(expected, response.json())



class CommandResultViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.command_result = async_to_sync(self.sandbox.execute)(
            self.user, {"commands": ["true"]}
        ).response.execution.all().first()
        self.client = Client()
        self.client.force_login(self.user)


    def test_get_single(self):
        command_result = self.client.get(
            reverse("django_sandbox:command_result", args=(self.command_result.pk,))
        )
        expected = {
            "status": True,
            "row":    dgeq.serialize(self.command_result),
        }
        self.assertEqual(200, command_result.status_code)
        self.assertEqual(expected, command_result.json())

    """ TODO
    def test_get_collection(self):
        commands = async_to_sync(self.sandbox.execute)(
            self.user, {"commands": ["true", "true"]}
        ).response.execution.all()
        command_result = self.client.get(
            reverse("django_sandbox:command_result_collection"),
            data={"response": f"[{commands[0].response.pk}"}
        )
        expected = {
            "status": True,
            "rows":   [
                dgeq.serialize(commands[0]),
                dgeq.serialize(commands[1]),
            ]
        }
        self.assertEqual(200, command_result.status_code)
        self.assertEqual(expected, command_result.json())
    """

    def test_get_404(self):
        command_result = self.client.get(reverse("django_sandbox:command_result", args=(9999,)))
        expected = {
            "status":  False,
            "message": "CommandResult matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, command_result.status_code)
        self.assertEqual(expected, command_result.json())


    def test_get_403(self):
        command = Client().get(
            reverse("django_sandbox:command_result", args=(self.command_result.pk,))
        )
        expected = {
            "status":  False,
            "message": "Missing view permission on CommandResult",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, command.status_code)
        self.assertEqual(expected, command.json())



class RequestViewTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test", is_superuser=True)
        self.request = async_to_sync(self.sandbox.execute)(self.user, {"commands": ["true"]})
        self.client = Client()
        self.client.force_login(self.user)


    def test_get_single(self):
        response = self.client.get(reverse("django_sandbox:request", args=(self.request.pk,)))
        # Encode and decode the expected output so that the date format match
        expected = json.loads(DjangoJSONEncoder().encode({
            "status": True,
            "row":    dgeq.serialize(self.request),
        }))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_collection(self):
        request1 = async_to_sync(self.sandbox.execute)(self.user, {"commands": ["true"]})
        request2 = async_to_sync(self.sandbox.execute)(self.user, {"commands": ["true"]})
        response = self.client.get(
            reverse("django_sandbox:request_collection"),
            data={"id": f"[{request1.pk}"}
        )
        # Encode and decode the expected output so that the date format match
        expected = json.loads(DjangoJSONEncoder().encode({
            "status": True,
            # Sorted by date so request 2 will be first
            "rows":   [
                dgeq.serialize(request2),
                dgeq.serialize(request1),
            ]
        }))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_404(self):
        response = self.client.get(reverse("django_sandbox:request", args=(9999,)))
        expected = {
            "status":  False,
            "message": "Request matching query does not exist.",
            "code":    ErrorCode.DoesNotExist.value
        }
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.json())


    def test_get_403(self):
        response = Client().get(reverse("django_sandbox:request", args=(self.request.pk,)))
        expected = {
            "status":  False,
            "message": "Missing view permission on Request",
            "code":    ErrorCode.PermissionDenied.value
        }
        self.assertEqual(403, response.status_code)
        self.assertEqual(expected, response.json())
