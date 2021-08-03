from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from .models import Consumer, ContactDetails, Spam


class ContactDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    ''' get all contacts of a user'''

    def get(self, request, *args, **kwargs):
        user = request.user.username
        try:
            consumer = Consumer.objects.filter(user=user)
            if consumer:
                contact = list(consumer[0].phone_number.all().values())
                return JsonResponse({"contact": list(contact)})
            else:
                return JsonResponse({"message": "please registered and save contacts"})
        except Exception as e:
            return JsonResponse({"error_message": " not havig contacts"}, status=400)

    ''' save contact into database'''

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user.username
        try:
            full_name = data['full_name']
            phone_number = data['phone_number']

            new_contact = ContactDetails.objects.create(full_name=full_name,
                                                        phone_number=phone_number)
            new_contact.save()
            consumer = Consumer.objects.get(user=user)
            consumer = Consumer.objects.filter(user=user)
            print(consumer[0])
            if consumer:
                consumer_object = consumer[0]
                consumer_object.phone_number.add(new_contact)
                return JsonResponse({"message": 'contact saved successfully'}, status=200)
            else:
                return JsonResponse({"message": 'User is not Registered !'}, status=200)

        except KeyError as e:
            message = f'{e.args[0]} is a required feild'
            return JsonResponse({"message": message}, status=400)

        except Exception as e:
            message = f'{e.args[0]} is a required feild'
            return JsonResponse({"error_message": message}, status=400)


class SpamView(APIView):
    permission_classes = [IsAuthenticated]

    '''get weather a phone_number is spam or not'''

    def get(self, request, *args, **kwargs):
        user = request.user.username
        data = request.data
        phone_number = data['phone_number']
        try:
            spam = Spam.objects.filter(phone_number=phone_number)
            if spam:
                return JsonResponse({"spam_status": True}, status=200)
            return JsonResponse({"spam_status": False}, status=200)
        except Exception as e:
            message = f'{e.args[0]} is a required feild'
            return JsonResponse({"error_message": message}, status=400)

    ''' added a phone_number into spam'''

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user.username
        try:
            phone_number = data['phone_number']
            spam = Spam.objects.filter(phone_number=phone_number)
            if spam:

                number_of_report = spam[0].number_of_report + 1
            else:
                number_of_report = 1
            new_spam = Spam.objects.create(phone_number=phone_number, number_of_report=number_of_report)
            new_spam.save()
            return JsonResponse({"message": 'contact added to spam successfully'}, status=200)

        except KeyError as e:
            message = f'{e.args[0]} is a required feild'
            return JsonResponse({"message": message}, status=400)

        except Exception as e:
            return JsonResponse({"error_message": " this user name is not registered"}, status=400)


class ContactSearchView(APIView):
    permission_classes = [IsAuthenticated]

    ''' get all contact which contains specific name'''

    def get(self, request, *args, **kwargs):
        user = request.user.username
        data = request.data
        try:
            partial_name = data['name']
            consumer = Consumer.objects.filter(user=user)
            contacts = list(consumer[0].phone_number.filter(full_name__contains=partial_name).values())
            partial_name_at_starting = []
            partial_name_in_between = []
            for individual_contact in contacts:
                if individual_contact['full_name'][:len(partial_name)] == partial_name:
                    partial_name_at_starting.append(individual_contact)
                else:
                    partial_name_in_between.append(individual_contact)
            return JsonResponse({
                "search_matching_name": partial_name_at_starting + partial_name_in_between,
                "number_contacts": len(contacts)
            })
        except Exception as e:
            message = f'{e.args[0]} is a required feild'
            return JsonResponse({"error_message": " this user name is not registered"}, status=400)
