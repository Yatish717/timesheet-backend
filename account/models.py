from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# from django.core.validators import MinValueValidator, MaxValueValidator




class CostCenter(models.Model):
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50, null=True)
    company_code = models.ForeignKey("account.CompanyCode",on_delete=models.PROTECT,related_name="costcenter_company")     ##added
   
    # organization = models.ForeignKey("Organization", on_delete=models.PROTECT, related_name='costcenter_organization')
    class Meta:
        db_table = "Aspl_CostCenter"
        verbose_name_plural = "CostCenters"
        # unique_together = ('name', 'number', 'organization')

    def __str__(self) -> str:
        return f"{self.name}_{self.number}"




class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=50, null=True)
    # organization = models.ForeignKey("Organization", on_delete=models.PROTECT, related_name='department_organization')
    class Meta:
        db_table = "Aspl_Department"
        verbose_name_plural = "Departments"
        # unique_together = ('name', 'organization')


    def __str__(self) -> str:
        return f"{self.id}_{self.name}"




class EmployeeRole(models.Model):
    roleName = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Aspl_EmployeeRole"
        verbose_name_plural = "EmployeeRoles"
        # unique_together = ('roleName', 'organization')
    ##  (1) admin , (2) manager, (3) team_leader,  (4) employee

    def __str__(self) -> str:
        return f"{self.id}_{self.roleName}"




class CompanyCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=50, null=True)
    # organization = models.ForeignKey("Organization", on_delete=models.PROTECT, related_name='companycode_organization')
    class Meta:
        db_table = "Aspl_CompanyCode"
        verbose_name_plural = "CompanyCodes"
        # unique_together = ('code', 'organization')

    def __str__(self) -> str:
        return f"{self.id}_{self.code}"




# class Organization(models.Model):
#     name = models.CharField(max_length=20, unique=True)
    
#     class Meta:
#         db_table = "Organization"
#         verbose_name_plural = "Organizations"

#     def __str__(self) -> str:
#         return f"{self.id}_{self.name}"



class OfficeBranch(models.Model):
    location = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Aspl_Branch"
        verbose_name_plural = "Aspl_Branches"

    def __str__(self) -> str:
        return f"{self.id}_{self.location}"




class EmployeeManager(BaseUserManager):
    def create_user(self, email, name, empID, department=None, companyCode=None, costcenter=None, role=None, branch=None,
                    password=None, password2=None, doj=None):

        if not email:
            raise ValueError('Users must have an email address')
        if not empID:
            raise ValueError('Users must have an empID')
        if not name:
            raise ValueError('Users must provide his full name')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            empID = empID,
            role= role,
            department = department,
            companyCode = companyCode,
            costcenter = costcenter,
            branch=branch,
            doj=doj
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, empID, password=None, **extra_fields):
        """Create a superuser with minimal required fields"""
        if not email:
            raise ValueError('Superuser must have an email address')
        if not name:
            raise ValueError('Superuser must have a name')
        if not empID:
            raise ValueError('Superuser must have an empID')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            empID=empID,
            is_superuser=True,
            is_verified=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user




class Employee(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=100)
    empID = models.CharField(max_length=20, primary_key=True, db_index=True)
    # organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='employee_department', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employee_department', null=True, blank=True)
    companyCode = models.ForeignKey(CompanyCode, on_delete=models.PROTECT, related_name='employee_companycode', null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True, default='')
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, related_name='employee_role', null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    costcenter = models.ForeignKey(CostCenter, on_delete=models.PROTECT, related_name='employe_costcenter', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    dol = models.DateField(null=True, blank=True)
    branch = models.ForeignKey(OfficeBranch, on_delete=models.PROTECT, related_name='employee_working_brach', null=True, blank=True)


    class Meta:
        db_table = "Aspl_Employee"
        ordering = ["empID"]
        verbose_name_plural = "Employees"
        # indexes = [
        #     models.Index(fields=['empID'], name='empID_index'),
        # ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'empID']

    objects = EmployeeManager()

    def __str__(self):
        return f"{self.name}_{self.empID}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        # return True
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser
    
        # ===== start change =====
    def save(self, *args, **kwargs):

        if self.costcenter:
            # Step 1: Auto assign companyCode
            self.companyCode = self.costcenter.company_code

            # Step 2: Auto assign department using costcenter.number
            from account.models import Department

            department = Department.objects.filter(
                name=self.costcenter.number
            ).first()

            if department:
                self.department = department

        super().save(*args, **kwargs)
    # ===== end change =====
