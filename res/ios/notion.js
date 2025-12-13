
// scriptable 에서 데이터베이스 쓰기 기능

class NotionObject {
  constructor(value) {
    this._value = value ?? {};
  }

  get value() {
    return this._value;
  }

  checkbox(properties, value) {
    const result = { [properties] : { "checkbox": value, "type": "checkbox" } }
    this._value = { ...this._value, ...result }
    return this
  }

  date(properties, start, end=null) {
    let payload = {}
    if (typeof start === "string") {
      payload = { date: { start: start, end: end }, type: "date" };
    }
    else if (start == null) {
      payload = { date: null, type: "date" };
    }
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  email(properties, value) {
    const payload = { email: value, type: "email" };
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  files(properties, name, url) {
    const payload = {
      type: "files",
      files: [
        {
          name: name,
          external: { url: url }
        }
      ]
    };

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  multiSelect(properties, value, ...values) {
    const resultArray = [
      { name: value },
      ...values.map(v => ({ name: v }))
    ];

    const payload = {
      multi_select: resultArray,
      type: "multi_select"
    };

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  number(properties, value) {
    const payload = { number: value, type: "number" };
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  people(properties, id, ...ids) {
    const resultArray = [
      { id: id },
      ...ids.map(peopleId => ({ id: peopleId }))
    ];

    const payload = {
      people: resultArray,
      type: "people"
    };

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  phoneNumber(properties, value) {
    const payload = { phone_number: value, type: "phone_number" };
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  relation(properties, id, ...ids) {
    const resultArray = [
      { id: id },
      ...ids.map(relationId => ({ id: relationId }))
    ];

    const payload = {
      relation: resultArray,
      type: "relation"
    };

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  text(properties, value) {
    let payload = {};

    if (typeof value === "string") {
      payload = {
        rich_text: [
          {
            text: { content: value },
            type: "text"
          }
        ]
      };
    } else if (value == null) {
      payload = { rich_text: [] };
    }

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  select(properties, value) {
    let payload = {};

    if (typeof value === "string") {
      payload = { select: { name: value }, type: "select" };
    } else if (value == null) {
      payload = { select: null };
    }

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  status(properties, value) {
    const payload = {
      status: { name: value },
      type: "status"
    };

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  title(properties, value) {
    let payload = {};

    if (typeof value === "string") {
      payload = {
        title: [
          {
            text: { content: value },
            type: "text"
          }
        ],
        type: "title"
      };
    } else if (value == null) {
      payload = { title: [], type: "title" };
    }

    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  url(properties, value) {
    const payload = { url: value, type: "url" };
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }
}

class Database {
  api_key;
  database_id;

  constructor(api_key, database_id) {
    this.api_key = api_key;
    this.database_id = database_id;
  }

  async write(notion_object) {
    const url = "https://api.notion.com/v1/pages"

    const request = await new Request(url)
		request.method = "POST"
		request.headers = {
			Accept: "application/json",
			"Notion-Version": "2022-06-28",
			"Content-Type": "application/json",
			Authorization: `Bearer ${this.api_key}`
		}
		request.body = JSON.stringify({
			parent: { database_id: this.database_id },
			properties: notion_object?.value
		})
		console.log(request)
		const response = await request.loadJSON()
		return response
  }
}

Script.complete()