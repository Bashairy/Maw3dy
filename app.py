from flask import Flask, render_template, request

from database.database import (
    add_booking,
    get_bookings,
    booking_exists
)

from bot.telegram_bot import notify_booking


app = Flask(
    __name__,
    template_folder="website/html"
)


@app.route("/", methods=["GET", "POST"])
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

        # حفظ الحجز في قاعدة البيانات
        add_booking(
            name,
            phone,
            date,
            time
        )

        # إرسال الإشعار إلى Telegram
        notify_booking(
            name,
            phone,
            date,
            time
        )

        # عرض رسالة نجاح جميلة في نفس الصفحة
        return render_template(
            "bookink.html",
            success=True,
            booking_name=name,
            booking_date=date,
            booking_time=time
        )

    return render_template("bookink.html")


@app.route("/bookings")
def bookings():

    all_bookings = get_bookings()

    return render_template(
        "bookings.html",
        bookings=all_bookings
    )


if __name__ == "__main__":
    app.run(debug=True)