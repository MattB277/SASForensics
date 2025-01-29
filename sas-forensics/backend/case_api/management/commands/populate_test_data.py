import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from case_api.models import Case, File, CaseChangelog

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create users
        users = []
        for i in range(1, 6):
            username = f"officer{i}"
            email = f"officer{i}@policescotland.uk"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "password": "securepassword"}
            )
            users.append(user)

        # Create cases and explicitly track their case numbers
        crime_types = ["Theft", "Fraud", "Homicide", "Arson", "Cybercrime"]
        locations = ["Edinburgh", "Glasgow", "Aberdeen", "Stirling", "Dundee"]
        statuses = ['new_evidence', 'new_collaboration', 'no_changes']
        created_case_numbers = []  # Track case numbers for this script
        cases = []

        for i in range(1, 11):
            case_number = f"CASE-{i:03d}"
            case = Case(
                case_number=case_number,
                crime_type=random.choice(crime_types),
                location=random.choice(locations),
                created_by=random.choice(users),
                status=random.choice(statuses),
            )
            case.save()
            case.assigned_users.set(random.sample(users, k=random.randint(1, 3)))
            case.refresh_from_db()
            cases.append(case)
            created_case_numbers.append(case_number)

        # Add files to cases
        if cases:
            first_case = cases[0]
            first_case_files = [
                "Day-1A_Incident-Report_Final3.pdf",
                "Day-1B_Firearms-NIBIN_Final.pdf",
                "Day-2_Cold-Case-Documents_Final2.pdf",
                "Day-3A_Investigative-Report_Final2.pdf",
                "Day-3B_Firearms-Comparison_Final2.pdf",
                "Day-4A_Firearms-SN-Restoration_Final2.pdf",
                "Day-4B_Latent-Prints_Final2.pdf",
                "Day-5A_DNA-Analysis-Report_Final2.pdf",
                "Day-5B_CODIS-Hit-Letter_Final2.pdf"
            ]
            for file_name in first_case_files:
                file_path = f"pdfs/{file_name}"
                File.objects.create(
                    file=file_path,
                    case_id=first_case,
                    file_type="pdf",
                )

        additional_files = [
            "crime_scene1.jpeg", "evidence1.mp4", "analysis.pdf",
            "report3.pdf", "evidence2.mp4", "scene2.jpeg"
        ]
        for file_name in additional_files:
            extension = file_name.split('.')[-1].lower()
            folder = 'pdfs' if extension == 'pdf' else 'images' if extension in ['jpeg', 'jpg', 'png'] else 'others'
            file_path = f"{folder}/{file_name}"
            File.objects.create(
                file=file_path,
                case_id=random.choice(cases[1:]),
                file_type=extension,
            )

        # Map changes to their corresponding types
        change_details_map = {
            "Added Evidence": [
                "Added new witness statement.",
                "Uploaded forensic analysis report.",
                "Submitted DNA analysis results."
            ],
            "Updated Information": [
                "Updated case status to 'active'.",
                "Added detailed crime scene descriptions.",
                "Corrected suspect details."
            ],
            "Assigned Detective": [
                "Assigned Detective Alexander McLean.",
                "Assigned Detective Fiona Campbell.",
                "Reassigned to Detective John Morrison."
            ],
            "Created Connection": [
                "Connected case with another cold case.",
                "Linked suspect to multiple cases.",
                "Identified potential connections with another region."
            ],
        }

        # Create case changelogs only for cases created in this script
        for _ in range(10):
            type_of_change = random.choice(list(change_details_map.keys()))
            change_details = random.choice(change_details_map[type_of_change])
            CaseChangelog.objects.create(
                case_id=random.choice([case for case in cases if case.case_number in created_case_numbers]),
                change_details=change_details,
                change_author=random.choice(users),
                type_of_change=type_of_change,
            )

