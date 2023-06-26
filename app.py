from flask import Flask, render_template, jsonify

app = Flask(__name__)

TARGETS = [
    {
        'id':1,
        'name':'Kathy Petersen',
        'relationship':'Mother',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'gardening'
            },
            {
                'id':2,
                'name':'rv'
            }
        ]
    },
    {
        'id':2,
        'name':'Dan Petersen',
        'relationship':'Father',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'fishing'
            },
            {
                'id':2,
                'name':'rv'
            }
        ]
    },
    {
        'id':3,
        'name':'Shaina Petersen',
        'relationship':'Wife',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'reading'
            },
            {
                'id':2,
                'name':'sewing'
            }
        ]
    },
    {
        'id':4,
        'name':'Renee Wilson',
        'relationship':'Sister',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'teaching'
            },
            {
                'id':2,
                'name':'gardening'
            }
        ]
    }
]


@app.route("/")
def friend_and_family_list():
    return render_template("target_list.html", title="Friends and Family", targets=TARGETS)

@app.route("/api/targets")
def return_target_list():
    return jsonify(TARGETS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)