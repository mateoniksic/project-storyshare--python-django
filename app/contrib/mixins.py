from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import UserProfile

class FollowMemberMixin:
    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        user_profile = get_object_or_404(UserProfile, pk=request.user.id)

        member_profile_id = request.POST.get(
            'formMemberFollow-member_profile_ID')
        member_profile = get_object_or_404(UserProfile, pk=member_profile_id)

        action = request.POST.get('formMemberFollow-submit')

        if action == 'follow':
            user_profile.following.add(member_profile)

        elif action == 'unfollow':
            user_profile.following.remove(member_profile)

        return render(request, self.template_name, context=context)
