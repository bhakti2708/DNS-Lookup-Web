from flask import Flask, render_template, request
import dns.resolver
import whois

app = Flask(__name__)


def get_records(domain, record_type):
    """Return DNS records as a list."""
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(answer) for answer in answers]
    except Exception:
        return []


@app.route("/", methods=["GET", "POST"])
def home():

    result = {}

    if request.method == "POST":

        domain = request.form.get("domain", "").strip()

        result["domain"] = domain

        records = ["A", "AAAA", "MX", "NS", "CNAME", "TXT"]

        for record in records:
            result[record] = get_records(domain, record)

        # WHOIS
        try:
            w = whois.whois(domain)

            result["whois"] = {
                "registrar": w.registrar or "Not Available",
                "creation": str(w.creation_date) if w.creation_date else "Not Available",
                "expiry": str(w.expiration_date) if w.expiration_date else "Not Available",
            }

        except Exception:

            result["whois"] = {
                "registrar": "Not Available",
                "creation": "Not Available",
                "expiry": "Not Available",
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)