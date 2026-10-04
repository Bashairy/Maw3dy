from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database.database import (
    add_booking,
    get_bookings,
    booking_exists,
    confirm_booking,
    delete_booking,
    create_db
)

from bot.telegram_bot import notify_booking


# ==========================================
# إنشاء التطبيق
# ==========================================

app = Flask(
    __name__,
    template_folder="website/html"
)

app.secret_key = "maw3dy-secret-key"

create_db()


# ==========================================
# بيانات دخول Admin
# ==========================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


# ==========================================
# الصفحة الرئيسية
# ==========================================

@app.route("/")
def index():

    return render_template("index.html")


# ==========================================
# تسجيل دخول Admin
# ==========================================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect(
                url_for("bookings")
            )

        else:

            error = "❌ اسم المستخدم أو كلمة المرور غير صحيحة."

    return render_template(
        "admin_login.html",
        error=error
    )


# ==========================================
# صفحة حجز المستخدم
# ==========================================

@app.route("/book", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        date = request.form["date"]
        time = request.form["time"]


        # التأكد من أن الموعد غير محجوز

        if booking_exists(date, time):

            return render_template(
                "bookink.html",
                error="⚠️ هذا الموعد محجوز بالفعل، يرجى اختيار وقت آخر."
            )


        # حفظ الحجز

        add_booking(
            name,
            phone,
            date,
            time
        )


        # إرسال إشعار Telegram

        notify_booking(
            name,
            phone,
            date,
            time
        )


        # رسالة نجاح

        return render_template(
            "bookink.html",
            success=True,
            booking_name=name,
            booking_date=date,
            booking_time=time
        )


    return render_template("bookink.html")


# ==========================================
# لوحة الحجوزات
# ==========================================

@app.route("/bookings")
def bookings():

    # حماية لوحة الإدارة

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    all_bookings = get_bookings()


    return render_template(
        "bookings.html",
        bookings=all_bookings
    )


# ==========================================
# تأكيد الحجز
# ==========================================

@app.route(
    "/confirm/<int:booking_id>",
    methods=["POST"]
)
def confirm(booking_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    confirm_booking(booking_id)


    return redirect(
        url_for("bookings")
    )


# ==========================================
# حذف الحجز
# ==========================================

@app.route(
    "/delete/<int:booking_id>",
    methods=["POST"]
)
def delete(booking_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )


    delete_booking(booking_id)


    return redirect(
        url_for("bookings")
    )


# ==========================================
# تسجيل خروج Admin
# ==========================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_logged_in",
        None
    )


    return redirect(
        url_for("index")
    )


# ==========================================
# تشغيل البرنامج
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)