from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


User = get_user_model()

ALLOW_CUSTOM_GROUP = True

SUBSCRIPTION_PERMISSIONS = [
            ('advanced', "Advanced perm"),
            ('pro', "Pro perm"),
            ('basic', "Basic Perm")
        ]

# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission,
                                         limit_choices_to={
                                              "content_type__app_label":  "subscriptions",
                                              "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS]
                                              },)

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

    def __str__(self):
            return self.name
    
class UserSubscription(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     subscription = models.ForeignKey(
          Subscription, on_delete=models.SET_NULL, null=True, blank=True)
     active = models.BooleanField(default=True)

     def __str__(self):
            return f"{self.user.username}:{self.subscription.name}"


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_object = user_sub_instance.subscription
    groups = subscription_object.groups.all()
    if not ALLOW_CUSTOM_GROUP:
        user.groups.set(groups)
    else:
        sub_qs = Subscription.objects.filter(active=True).exclude(id=subscription_object.id)
        sub_groups = sub_qs.values_list("groups__id", flat=True)
        group_ids = groups.values_list("id", flat=True)
        current_groups = user.groups.all().values_list("id", flat=True)
        current_groups_set = set(current_groups) - set(sub_groups)
        group_ids = list(set(group_ids) | current_groups_set)
        user.groups.set(group_ids)

post_save.connect(user_sub_post_save, sender=UserSubscription)