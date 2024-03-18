from django.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название муниципального образования")

    class Meta:
        verbose_name = "Муниципальное образование"
        verbose_name_plural = "Муниципальные образования"
        app_label = "applications_app"

    def __str__(self):
        return self.name


class School(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name="Муниципальное образование",
                                     related_name="schools")
    name = models.CharField(max_length=100, verbose_name="Название школы")

    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"
        app_label = "applications_app"

    def __str__(self):
        return self.name


class Applicant(models.Model):
    telegram_id = models.CharField(max_length=512, unique=True, verbose_name="Telegram ID заявителя")
    phone_number = models.CharField(max_length=32, unique=True, verbose_name="Номер телефона заявителя")

    class Meta:
        verbose_name = "Заявитель"
        verbose_name_plural = "Заявители"
        app_label = "applications_app"

    def __str__(self):
        return self.phone_number


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="Заявитель")

    full_name = models.CharField(max_length=256, verbose_name="ФИО заявителя")

    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Школа")

    child_full_name = models.CharField(max_length=256, verbose_name="ФИО ребенка")
    CHILD_GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]
    child_gender = models.CharField(max_length=30, choices=CHILD_GENDER_CHOICES, verbose_name="Пол ребенка")

    child_age = models.IntegerField(verbose_name="Возраст ребенка")
    received_offer = models.BooleanField(verbose_name="Получали предложение от школы")

    DURATION_CHOICES = [
        ('На 21 день', 'На 21 день'),
        ('До конца учебного года', 'До конца учебного года'),
    ]
    duration = models.CharField(max_length=30, choices=DURATION_CHOICES, null=True, blank=True,
                                verbose_name="Срок выезда")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        app_label = "applications_app"

    def __str__(self):
        return f"{self.full_name} - {self.child_full_name}"
