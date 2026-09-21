from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import json
import re

JOBS = [
    {"title": "SSC CGL — Graduate Level", "organization": "Staff Selection Commission", "category": "government", "course": "Any Graduate", "location": "All India"},
    {"title": "Junior Data Analyst", "organization": "NxtWave Technologies", "category": "private", "course": "B.Tech / B.Com", "location": "Bengaluru / Remote"},
    {"title": "Nursing Officer — NORCET", "organization": "AIIMS India", "category": "government", "course": "B.Sc Nursing", "location": "Multiple cities"},
    {"title": "RRB NTPC — Graduate Posts", "organization": "Railway Recruitment Board", "category": "government", "course": "Any Graduate", "location": "All India"},
    {"title": "RBI Assistant", "organization": "Reserve Bank of India", "category": "government", "course": "Any Graduate", "location": "Regional offices"},
    {"title": "IBPS PO — Probationary Officer", "organization": "Institute of Banking Personnel Selection", "category": "government", "course": "B.Com / Any Graduate", "location": "All India"},
    {"title": "UPSC Civil Services Examination", "organization": "Union Public Service Commission", "category": "government", "course": "Any Graduate", "location": "All India"},
    {"title": "NABARD Grade A — Agriculture", "organization": "National Bank for Agriculture and Rural Development", "category": "government", "course": "B.Sc Agriculture", "location": "All India"},
    {"title": "FCI Assistant Grade III", "organization": "Food Corporation of India", "category": "government", "course": "B.Sc Agriculture", "location": "Zone-wise"},
    {"title": "ESIC Nursing Officer", "organization": "Employees' State Insurance Corporation", "category": "government", "course": "B.Sc Nursing", "location": "Multiple states"},
    {"title": "Graduate Software Engineer", "organization": "Product Technology Company", "category": "private", "course": "B.Tech", "location": "Hyderabad / Remote"},
    {"title": "Junior Accounts Executive", "organization": "Growing Finance Team", "category": "private", "course": "B.Com", "location": "Pune / Hybrid"},
]


@require_GET
def jobs(request):
    query = request.GET.get("q", "").strip().lower()
    category = request.GET.get("category", "").strip().lower()
    matches = [
        job for job in JOBS
        if (not query or query in f"{job['title']} {job['organization']} {job['course']}".lower())
        and (not category or job["category"] == category)
    ]
    return JsonResponse({"results": matches})


@require_POST
def register(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Send valid JSON."}, status=400)

    name = str(payload.get("name", "")).strip()
    mobile = re.sub(r"\D", "", str(payload.get("mobile", "")))
    course = str(payload.get("course", "")).strip()
    if not name or len(mobile) != 10 or not course:
        return JsonResponse({"error": "Name, course, and a valid 10-digit mobile number are required."}, status=400)
    return JsonResponse({"message": f"Registration successful! Confirmation sent to {mobile}.", "student": {"name": name, "course": course}})


@require_POST
def applications(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Send valid JSON."}, status=400)
    job = str(payload.get("job", "")).strip()
    name = str(payload.get("name", "")).strip()
    mobile = re.sub(r"\D", "", str(payload.get("mobile", "")))
    email = str(payload.get("email", "")).strip()
    if not job or not name or len(mobile) != 10 or "@" not in email:
        return JsonResponse({"error": "Job, name, valid mobile number, and email are required."}, status=400)
    return JsonResponse({"message": "Application submitted.", "application": {"job": job, "name": name, "mobile": mobile, "email": email, "status": "Submitted"}}, status=201)


@require_GET
def notifications(request):
    return JsonResponse({"last_checked_at": "now", "source_mode": "approved-public-seeds", "results": []})
