from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from common.decorators import http



def view(request):
    return HttpResponse(status=200)



class RequireHttpMethodsAsyncTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.view = view
    
    
    async def test_multiple_method_ok(self):
        view = await http.require_http_methods_async(["GET", "POST"])(self.view)
        
        request = self.factory.get('/customer/details')
        request.user = AnonymousUser()
        response = await view(request)
        self.assertEqual(response.status_code, 200)
        
        request = self.factory.post('/customer/details')
        request.user = AnonymousUser()
        response = await view(request)
        self.assertEqual(response.status_code, 200)
        
        request = self.factory.delete('/customer/details')
        request.user = AnonymousUser()
        response = await view(request)
        self.assertEqual(response.status_code, 405)
        
        request = self.factory.patch('/customer/details')
        request.user = AnonymousUser()
        response = await view(request)
        self.assertEqual(response.status_code, 405)
