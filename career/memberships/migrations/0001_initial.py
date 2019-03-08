# Generated by Django 2.1 on 2019-01-09 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('membership_type', models.CharField(choices=[('Enterprise', 'Ent'), ('Professional', 'Pro'), ('Free', 'Free')], default='Free', max_length=20)),
                ('price', models.IntegerField(default=15)),
                ('paystack_plan_id', models.CharField(default='0x67618b6d', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaystackPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('user_key', models.CharField(default='0x3d7a2ba', max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paystack_subscription_id', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paystack_customer_id', models.CharField(max_length=50)),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='memberships.Membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subscription',
            name='user_membership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memberships.UserMembership'),
        ),
    ]
