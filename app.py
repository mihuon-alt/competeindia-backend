from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, Competition, Submission, Subscriber
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///competeindia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')

CORS(app)
db.init_app(app)

# ── SEED DATA ─────────────────────────────────
def seed_competitions():
    if Competition.query.count() > 0:
        return
    comps = [
        Competition(name="IRIS National Science Fair", category="science",
            description="India's biggest student science competition run with Intel & DST. Winners represent India at Intel ISEF internationally.",
            deadline="Dec–Jan (Annual)", eligibility="Class 6–12", organizer="DST & Intel India",
            link="https://irisfaire.in", level="National", featured=True),
        Competition(name="National Children's Science Congress (NCSC)", category="science",
            description="DST-sponsored congress where young scientists present research on environment, health and technology themes.",
            deadline="Sep–Oct (Annual)", eligibility="Class 7–10", organizer="NCSTC / DST",
            link="https://ncstc.gov.in", level="National"),
        Competition(name="INSPIRE Awards – MANAK", category="science",
            description="Government of India scheme to inspire 1 million school children to identify problems and develop innovations.",
            deadline="Oct–Nov (Annual)", eligibility="Class 6–10", organizer="NIF / DST",
            link="https://www.inspireawards-dst.gov.in", level="National"),
        Competition(name="Young Scientist Programme (ISRO Yuvika)", category="science",
            description="ISRO's flagship programme for Class 9 students to learn about space science at ISRO centres directly.",
            deadline="Jan–Feb (Annual)", eligibility="Class 9", organizer="ISRO",
            link="https://www.isro.gov.in/yuvika", level="National", featured=True),
        Competition(name="KVPY Fellowship", category="science",
            description="Prestigious DST fellowship for students passionate about research in Basic Sciences. Includes generous scholarship.",
            deadline="May–Jun (Annual)", eligibility="Class 11–12 & 1st year BSc", organizer="IISc / DST",
            link="https://kvpy.iisc.ac.in", level="National"),
        Competition(name="Jawaharlal Nehru National Science Exhibition", category="science",
            description="NCERT's flagship science exhibition for school students. State-level selections lead to national exhibition.",
            deadline="Aug–Sep (Annual)", eligibility="Class 6–12", organizer="NCERT",
            link="https://ncert.nic.in", level="National"),
        Competition(name="DELMUN – Delhi International Model UN", category="mun",
            description="One of India's most prestigious MUN conferences with international delegates from 15+ countries and 12 committees.",
            deadline="Feb–Mar (Annual)", eligibility="Class 8–12", organizer="DELMUN Secretariat",
            link="https://delmun.com", level="National", featured=True),
        Competition(name="JNUMUN – JNU Model United Nations", category="mun",
            description="Hosted by Jawaharlal Nehru University. One of the most academically rigorous MUNs in India.",
            deadline="Oct–Nov (Annual)", eligibility="Class 10–College", organizer="JNU MUN Society",
            link="https://jnumun.in", level="National"),
        Competition(name="BMUN – Bangalore Model UN", category="mun",
            description="South India's largest MUN conference. Excellent for first-time delegates with beginner-friendly committees.",
            deadline="Mar–Apr (Annual)", eligibility="Class 7–12", organizer="BMUN Committee",
            link="https://bmun.in", level="Regional"),
        Competition(name="AIMUN – All India Model UN", category="mun",
            description="Pan-India MUN where school delegations represent schools from across India. Strong debate culture.",
            deadline="Jan–Feb (Annual)", eligibility="Class 9–12", organizer="AIMUN Society",
            link="https://aimun.in", level="National"),
        Competition(name="National Science Quiz – CBSE", category="quiz",
            description="Official CBSE national quiz covering Physics, Chemistry, Biology and Environmental Science.",
            deadline="Jan–Feb (Annual)", eligibility="Class 9–12", organizer="CBSE",
            link="https://cbse.gov.in", level="National"),
        Competition(name="Bournvita Quiz Contest", category="quiz",
            description="One of India's longest-running school quiz competitions. Regional and national rounds across India.",
            deadline="Jul–Aug (Annual)", eligibility="Class 6–10", organizer="Mondelez India",
            link="https://bournvitaquiz.com", level="National", featured=True),
        Competition(name="National Science Olympiad – SOF", category="quiz",
            description="National Science Olympiad testing scientific reasoning. School, zonal and international levels with medals.",
            deadline="Sep–Oct (Annual)", eligibility="Class 1–12", organizer="Science Olympiad Foundation",
            link="https://sofworld.org", level="International"),
        Competition(name="Indian National Mathematical Olympiad (INMO)", category="olympiad",
            description="Prestigious national math olympiad. Top performers represent India at the International Mathematical Olympiad.",
            deadline="Oct–Dec (Prelim RMO)", eligibility="Class 9–12", organizer="HBCSE / TIFR",
            link="https://olympiads.hbcse.tifr.res.in", level="National → International", featured=True),
        Competition(name="Indian National Physics Olympiad (INPhO)", category="olympiad",
            description="Selects students for International Physics Olympiad (IPhO). Includes theory and experimental rounds.",
            deadline="Nov–Jan (Prelim NSEP)", eligibility="Class 11–12", organizer="HBCSE",
            link="https://olympiads.hbcse.tifr.res.in", level="National → International"),
        Competition(name="Indian National Chemistry Olympiad (INChO)", category="olympiad",
            description="Selects students for International Chemistry Olympiad (IChO). Theory and lab-based examination.",
            deadline="Nov–Jan (Prelim NSEC)", eligibility="Class 11–12", organizer="HBCSE",
            link="https://olympiads.hbcse.tifr.res.in", level="National → International"),
        Competition(name="SOF International Mathematics Olympiad", category="olympiad",
            description="School-level maths olympiad with school, zonal and international rounds. Millions of participants.",
            deadline="Oct–Nov (Annual)", eligibility="Class 1–12", organizer="Science Olympiad Foundation",
            link="https://sofworld.org", level="International"),
        Competition(name="IOI – Informatics Olympiad India Selection", category="olympiad",
            description="Selection camp for India's IOI team. Tests competitive programming and algorithmic problem solving.",
            deadline="Jan–Feb (Annual)", eligibility="Class 9–12", organizer="HBCSE / IARCS",
            link="https://www.iarcs.org.in", level="International"),
        Competition(name="Smart India Hackathon (SIH) Junior", category="tech",
            description="Government of India's hackathon for school students. Build solutions for real national problems. Prize up to ₹1L.",
            deadline="Jan–Feb (Annual)", eligibility="Class 8–12", organizer="MHRD / AICTE",
            link="https://www.sih.gov.in", level="National", featured=True),
        Competition(name="Atal Tinkering Marathon", category="tech",
            description="Niti Aayog's innovation challenge for students in Atal Tinkering Labs. Problem-solving and prototyping.",
            deadline="Oct–Nov (Annual)", eligibility="Class 6–12 (ATL schools)", organizer="Atal Innovation Mission",
            link="https://aim.gov.in", level="National"),
        Competition(name="Technothlon – IIT Guwahati", category="tech",
            description="India's largest school-level tech fest by IIT Guwahati students. Puzzle and tech challenges.",
            deadline="Jun–Jul (Annual)", eligibility="Class 9–12", organizer="IIT Guwahati",
            link="https://technothlon.techniche.org", level="National"),
        Competition(name="Google Code to Learn", category="tech",
            description="Google's coding competition encouraging creative use of technology to solve community problems.",
            deadline="Mar–Apr (Annual)", eligibility="Class 5–10", organizer="Google India",
            link="https://codetolearn.withgoogle.com", level="National"),
        Competition(name="National Children's Art Exhibition – NGMA", category="arts",
            description="National Gallery of Modern Art's annual art competition for school children. Winners displayed nationally.",
            deadline="Oct–Nov (Annual)", eligibility="Class 1–12", organizer="NGMA India",
            link="https://ngmaindia.gov.in", level="National"),
        Competition(name="Camlin Art Foundation Competition", category="arts",
            description="One of India's biggest school art competitions. Categories include painting, sketching and digital art.",
            deadline="Sep–Oct (Annual)", eligibility="Class 1–12", organizer="Camlin India",
            link="https://camlin.com", level="National"),
        Competition(name="Bal Shree Award", category="arts",
            description="Government of India's prestigious award for exceptional talent in arts, literature and performing arts for children.",
            deadline="Apr–May (Annual)", eligibility="6–16 years", organizer="National Bal Bhavan",
            link="https://nbbindia.com", level="National"),
        Competition(name="Commonwealth Essay Competition", category="writing",
            description="World's oldest and largest writing competition for students in Commonwealth countries including India.",
            deadline="Mar–Jun (Annual)", eligibility="Under 18", organizer="Royal Commonwealth Society",
            link="https://www.commonwealthessay.com", level="International", featured=True),
        Competition(name="Times NIE Write India", category="writing",
            description="Times of India's creative writing competition for school students with mentoring from established authors.",
            deadline="Rolling monthly", eligibility="Class 6–12", organizer="Times of India NIE",
            link="https://timesnie.com", level="National"),
        Competition(name="CBSE Expression Series", category="writing",
            description="CBSE's national level writing, art and multimedia competition for school students on thematic topics.",
            deadline="Oct–Nov (Annual)", eligibility="Class 3–12", organizer="CBSE",
            link="https://cbse.gov.in", level="National"),
        Competition(name="MSME Innovative Ideas Competition", category="science",
            description="Ministry of MSME competition encouraging innovative ideas and entrepreneurship among school and college students.",
            deadline="Dec–Jan (Annual)", eligibility="School & College Students", organizer="Ministry of MSME",
            link="https://msme.gov.in", level="National"),
        Competition(name="National Startup Challenge – School Edition", category="tech",
            description="Startup India initiative where school students pitch business ideas to mentors and win incubation support.",
            deadline="Feb–Mar (Annual)", eligibility="Class 9–12", organizer="DPIIT / Startup India",
            link="https://startupindia.gov.in", level="National"),
    ]
    for c in comps:
        db.session.add(c)
    db.session.commit()
    print(f"Seeded {len(comps)} competitions.")

# ── ROUTES ────────────────────────────────────

@app.route('/api/competitions', methods=['GET'])
def get_competitions():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip().lower()
    featured_only = request.args.get('featured', 'false') == 'true'

    query = Competition.query.filter_by(approved=True)

    if category != 'all':
        query = query.filter_by(category=category)

    if featured_only:
        query = query.filter_by(featured=True)

    comps = query.order_by(Competition.featured.desc(), Competition.created_at.desc()).all()

    if search:
        comps = [c for c in comps if
            search in c.name.lower() or
            search in c.description.lower() or
            search in c.organizer.lower() or
            search in c.category.lower()]

    return jsonify([c.to_dict() for c in comps])


@app.route('/api/competitions/<int:comp_id>', methods=['GET'])
def get_competition(comp_id):
    comp = Competition.query.get_or_404(comp_id)
    return jsonify(comp.to_dict())


@app.route('/api/competitions/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'total': Competition.query.filter_by(approved=True).count(),
        'categories': {
            'science': Competition.query.filter_by(category='science', approved=True).count(),
            'mun': Competition.query.filter_by(category='mun', approved=True).count(),
            'quiz': Competition.query.filter_by(category='quiz', approved=True).count(),
            'olympiad': Competition.query.filter_by(category='olympiad', approved=True).count(),
            'tech': Competition.query.filter_by(category='tech', approved=True).count(),
            'arts': Competition.query.filter_by(category='arts', approved=True).count(),
            'writing': Competition.query.filter_by(category='writing', approved=True).count(),
        }
    })


@app.route('/api/submit', methods=['POST'])
def submit_competition():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('link'):
        return jsonify({'error': 'Name and link are required'}), 400

    sub = Submission(
        name=data.get('name'),
        category=data.get('category', 'other'),
        description=data.get('description', ''),
        deadline=data.get('deadline', ''),
        eligibility=data.get('eligibility', ''),
        link=data.get('link'),
        organizer=data.get('organizer', ''),
        submitted_by=data.get('email', '')
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify({'message': 'Submitted successfully! We will review within 24 hours.'}), 201


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = (data or {}).get('email', '').strip()
    if not email or '@' not in email:
        return jsonify({'error': 'Valid email required'}), 400

    if Subscriber.query.filter_by(email=email).first():
        return jsonify({'message': 'Already subscribed!'}), 200

    sub = Subscriber(email=email)
    db.session.add(sub)
    db.session.commit()
    return jsonify({'message': 'Subscribed! You will get alerts for new competitions.'}), 201


# ── ADMIN ROUTES (basic, add auth in production) ──

@app.route('/api/admin/submissions', methods=['GET'])
def get_submissions():
    subs = Submission.query.order_by(Submission.created_at.desc()).all()
    return jsonify([s.to_dict() for s in subs])


@app.route('/api/admin/submissions/<int:sub_id>/approve', methods=['POST'])
def approve_submission(sub_id):
    sub = Submission.query.get_or_404(sub_id)
    comp = Competition(
        name=sub.name, category=sub.category, description=sub.description,
        deadline=sub.deadline, eligibility=sub.eligibility, link=sub.link,
        organizer=sub.organizer, approved=True
    )
    db.session.add(comp)
    sub.approved = True
    db.session.commit()
    return jsonify({'message': 'Approved and added to competitions!'})


@app.route('/api/admin/competitions/<int:comp_id>', methods=['DELETE'])
def delete_competition(comp_id):
    comp = Competition.query.get_or_404(comp_id)
    db.session.delete(comp)
    db.session.commit()
    return jsonify({'message': 'Deleted'})


@app.route('/api/admin/competitions/<int:comp_id>/feature', methods=['POST'])
def toggle_feature(comp_id):
    comp = Competition.query.get_or_404(comp_id)
    comp.featured = not comp.featured
    db.session.commit()
    return jsonify({'featured': comp.featured})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_competitions()
    app.run(debug=True, port=5000)
