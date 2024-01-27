from pykeyboard import InlineButton, InlineKeyboard
from pyrogram import filters
from requests import get

from bot import API, CHANNEL, bot


@bot.on_message(filters.command("semesters"))
async def start(client, message):
    semesters = get(API + "semesters/").json()
    inline_buttons = [
        InlineButton(str(semester["name"]), f"semester_{semester['id']}")
        for semester in semesters
    ]
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(*inline_buttons)

    return await message.reply_text(
        f"Hello {message.from_user.first_name}, I'm here to find resources for VU CSE Depertment. Master is still devoloping me, so don't expect much.",
        reply_markup=keyboard,
    )


@bot.on_callback_query(filters.regex(r"semester(.*?)"))
async def helpbtn(_, query):
    i = query.data.replace("semester_", "")
    courses = get(API + f"semester/{i}").json()
    print(courses)
    inline_buttons = [
        InlineButton(str(course["code"]), f"course_{course['id']}")
        for course in courses.get("course")
    ]
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(*inline_buttons)
    keyboard.row(InlineButton("Back", "homepage"))
    text = f"This is the courses for {courses.get('name')}"
    await query.message.edit(text=text, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"course(.*?)"))
async def coursecallback(app, query):
    i = query.data.replace("course_", "")
    course = get(API + f"course/{i}").json()
    if not course.get("resource"):
        return await app.answer_callback_query(
            query.id,
            text="Sorry, We don't have any resources for this course. If you have any, please contact us.",
            show_alert=True,
        )
    print(course)
    inline_buttons = [
        InlineButton(str(resource["name"]), f"resource_{resource['id']}")
        for resource in course.get("resource")
    ]
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(*inline_buttons)
    print("\n")
    print(course.get("id"))
    keyboard.row(InlineButton("Back", f"semester_{course.get('semester').get('id')}"))
    text = f"This is the resources for {course.get('name')}"
    await query.message.edit(text=text, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"resource(.*?)"))
async def resourcecallback(app, query):
    i = query.data.replace("resource_", "")
    resource = get(API + f"resource/{i}").json()
    print(resource)
    inline_buttons = [
        InlineButton(str(resource["name"]), f"file_{resource['m_id']}")
        for resource in resource.get("tg")
    ]
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(*inline_buttons)
    keyboard.row(InlineButton("Back", f"course_{resource.get('course').get('id')}"))
    text = f"**[{resource.get('name')}]({resource.get('link')})**\n\n{resource.get('description')}"
    await query.message.edit(text=text, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"file(.*?)"))
async def filecallback(app, query):
    i = query.data.replace("file_", "")

    await app.copy_message(query.from_user.id, CHANNEL, int(i))


@bot.on_callback_query(filters.regex(r"homepage(.*?)"))
async def start(client, query):
    semesters = get(API + "semesters/").json()
    inline_buttons = [
        InlineButton(str(semester["name"]), f"semester_{semester['id']}")
        for semester in semesters
    ]
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(*inline_buttons)

    return await query.message.edit(
        f"Hello {query.from_user.first_name}, I'm here to find resources for VU CSE Depertment. Master is still devoloping me, so don't expect much.",
        reply_markup=keyboard,
    )
