from flask import Flask, render_template, request, jsonify
import x
import uuid
app = Flask(__name__)
 
###########################################
@app.post("/signup")
def signup():
  try:
    user_first_name = x.validate_user_first_name()
    user_last_name = x.validate_user_last_name()
    user_username = x.validate_user_username()
    user_pk = uuid.uuid4().hex
    db, cursor = x.db()
    q = "INSERT INTO users VALUES (%s, %s, %s, %s)"
    cursor.execute(q, (user_pk, user_first_name, user_last_name, user_username))
    db.commit()
    return "ok"
  except Exception as ex:

    try:
        print(ex, flush=True) # ('User first name minimal 2 characters', 400) # tuple
        return ex.args[0], ex.args[1]
    except: Exception as e:
        print(e, flush=True)
        if "Duplicate entry" in str(e) and "user_username" in str(e):
            return "user_username already exists", 400
    finally:
        pass

    """
    # 1062 (23000): Duplicate entry 'santi' for key 'user_username'
    print(ex, flush=True) # ('User first name minimal 2 characters', 400) # tubble
    return ex.args[0], ex.args[1]
    """


  finally:
    if "cursor" in locals(): cursor.close()
    if "db" in locals(): db.close()