
// scriptable 에서 데이터베이스 쓰기 기능

class NotionObject {
  constructor(value) {
    if (value == null) {
      this._value = {};
      return;
    }
    this._value = value;
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

  files (properties, value) {
    console.log("files 는 아직 미구현")
    return this;
  }

  formula(properties, value) {
    console.log("formula 는 아직 미구현")
    const payload = { formula: { expression: value }, type: "formula" }
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  multi_select(properties, value) {
    console.log("multi_select 는 아직 미구현")
    return this;
  }

  number(properties, value) {
    const payload = { number: value, type: "number" };
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  people(properties, value) {
    console.log("people 는 아직 미구현")
    return this;
  }

  phoneNumber(properties, value) {
    const payload = { phone_number: value, type: "phone_number" };
    const result = { [properties]: payload };
    this._value = { ...this._value, ...result };
    return this;
  }

  place(properties, value) {
    console.log("place 는 아직 미구현")
    return this;
  }

  relation(properties, value) {
    console.log("relation 는 아직 미구현")
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

  rollup(properties, value) {
    console.log("rollup 는 아직 미구현")
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
    console.log("status 는 아직 미구현")
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

  unique_id(properties, value) {
    console.log("unique_id 는 아직 미구현")
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