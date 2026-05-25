// @ts-nocheck


//#region 1. 추상 클래스 및 기반 인터페이스 정의
// 파이썬의 NotionBase 역할
class NotionBase {
  /**
   * 
   * @param {string} apiKey 
   * @param {string} id 
   * @param {string} object 
   */
  constructor(apiKey, id, object) {
    if (this.constructor === NotionBase) {
        throw new TypeError("추상 클래스 NotionBase는 직접 인스턴스화할 수 없습니다.");
    }
    this.apiKey = apiKey;
    this.id = id;
    this.object = object;
    this.archived = false; // 삭제했는지에 관한 정보
  }

  /**
   * 헤더에 버전을 추가해서 리턴
   * @param {"2025-09-03" | "2022-06-28"} version - 노션 API 버전 정보
   */
  _addHeaders(version) {
    return {
      "Accept": "application/json",
      "Notion-Version": version,
      "Content-Type": "application/json",
      "Authorization": `Bearer ${this.apiKey}`
    };
  }
}


// 파이썬의 Read, Write, Update, Remove 인터페이스 역할
// JS에서는 인터페이스가 없으므로 추상 메서드를 가진 클래스로 구현합니다.
class Read {
  constructor() { if (this.constructor === Read) throw new TypeError("인터페이스는 인스턴스화할 수 없습니다."); }
  read() { throw new Error("read() 메서드가 구현되지 않았습니다."); }
}


class Write {
  constructor() { if (this.constructor === Write) throw new TypeError("인터페이스는 인스턴스화할 수 없습니다."); }
  write() { throw new Error("write() 메서드가 구현되지 않았습니다."); }
}


class Update {
  constructor() { if (this.constructor === Update) throw new TypeError("인터페이스는 인스턴스화할 수 없습니다."); }
  update() { throw new Error("update() 메서드가 구현되지 않았습니다."); }
}


class Remove {
  constructor() { if (this.constructor === Remove) throw new TypeError("인터페이스는 인스턴스화할 수 없습니다."); }
  remove() { throw new Error("remove() 메서드가 구현되지 않았습니다."); }
}


// 파이썬의 DictValueBase 역할
class DictValueBase {
  constructor(value = null) {
    if (this.constructor === DictValueBase) {
        throw new TypeError("추상 클래스 DictValueBase는 직접 인스턴스화할 수 없습니다.");
    }
    this._value = value === null ? {} : value;
  }

  get value() {
    return this._value;
  }
}


// 파이썬의 ListValueBase 역할
class ListValueBase {
  constructor(value = null) {
    if (this.constructor === ListValueBase) {
        throw new TypeError("추상 클래스 ListValueBase는 직접 인스턴스화할 수 없습니다.");
    }
    this._value = value === null ? [] : value;
  }

  get value() {
    return this._value;
  }
}
//#endregion


//#region 2. 블록 오브젝트 정의
/**
 * 직접 사용하진 않음
 * 
 * 그런데 다른 텍스트 관련 블록 오브젝트에서 공통으로 사용됨
 */
class TextObject {
  object(value) {
    if (typeof value === 'string') {
      return { "rich_text": [ { "text": { "content": value }, "type": "text" } ] };
    } else if (value === null || value === undefined) {
      return { "rich_text": [] };
    }
    return {};
  }
  get(value) {
    const values = value["rich_text"];
    if (!values || values.length === 0) {
      return null;
    }

    const _value = values[0];
    return _value["plain_text"];
  }
}


/**
 * 직접 사용하지 않음
 * 
 * 그런데 다른 파일 관련 블록 오브젝트에서 공통으로 사용됨
 */
class FileObject {
  object(url) {
    if (typeof url === 'string') {
      return {
        "file": {
          "type": "external",
          "external": { "url": url }
        }
      };
    } else if (url === null || url === undefined) {
      return { "file": null };
    }
    return {};
  }
  get(value) {
    const type = value["type"];
    if (!value[type]) {
      return null;
    }
    return {
      "name": value["name"],
      "file": value[type]["url"]
    };
  }
}


class AudioBlockObject {
  object(url) {
    console.log("audio 정보", url);
    return new FileObject().object(url);
  }
  get(value) {
    return value["audio"]["external"]["url"];
  }
}


class BookmarkBlockObject {
  object(value) {
    // 북마크에 url 타입 있으면 안댐 { "url": value, "type": "url" } 이렇게 안댐
    return { "url": value };
  }
  get(value) {
    return value["url"];
  }
}


class BreadcrumbBlockObject {
  object(value) {
    console.log("Breadcrumb 정보", value);
    return {};
  }
  get(value) {
    console.log("Breadcrumb 정보", value);
    return {};
  }
}


class BulletedListItemBlockObject {
  object(value) {
    console.log("bulleted_list_item 정보", value);
    return {};
  }
  get(value) {
    console.log("bulleted_list_item 정보", value);
    return {};
  }
}


class CalloutBlockObject {
  // 파이썬의 키워드 전용 인자(*, icon="💡", color="gray_background")는 JS 객체 구조분해할당으로 구현합니다.
  object(value, { icon = "💡", color = "gray_background" } = {}) {
    const result = { "callout": new TextObject().object(value) };
    result["callout"]["icon"] = { "emoji": icon, "type": "emoji" };
    result["callout"]["color"] = color;
    return result;
  }
  get(value) {
    const iconType = value["icon"]["type"];
    return {
      "icon": value["icon"][iconType],
      "text": new TextObject().get(value)
    };
  }
}


class ChildDatabaseBlockObject {
  object(value) {
    console.log("child_database 정보", value);
    return {};
  }
  get(value) {
    console.log("child_database 정보", value);
    return {};
  }
}


class ChildPageBlockObject {
  object(value) {
    console.log("child_page 정보", value);
    return { "child_page": { "title": value } };
  }
  get(value) {
    return value["title"];
  }
}


class CodeBlockObject {
  object(value) {
    return new TextObject().object(value);
  }
  get(value) {
    const text = new TextObject().get(value);
    if (text === null) return null;
    return {
      "code": text,
      "language": value["language"]
    };
  }
}


class ColumnListAndColumnBlockObject {
  object(value) {
    console.log("ColumnListAndColumn 정보", value);
    return {};
  }
  get(value) {
    console.log("ColumnListAndColumn 정보", value);
    return {};
  }
}


class DividerBlockObject {
  object(value) {
    console.log("divider 정보", value);
    return { "type": "divider", "divider": {} };
  }
  get(value) {
    console.log("divider 정보", value);
    return {};
  }
}


class EmbedBlockObject {
  object(url) {
    console.log("embed 정보", url);
    return {};
  }
  get(value) {
    console.log("embed 정보", value);
    return value["embed"]["url"];
  }
}


class EquationBlockObject {
  object(value) {
    console.log("equation 정보", value);
    return {};
  }
  get(value) {
    console.log("equation 정보", value);
    return value["equation"]["expression"];
  }
}


class FileBlockObject {
  object(value) {
    console.log("file 정보", value);
    return new FileObject().object(value);
  }
  get(value) {
    return new FileObject().get(value);
  }
}


class Heading123BlockObject {
  object(value) {
    return new TextObject().object(value);
  }
  get(value) {
    return new TextObject().get(value);
  }
}


class ImageBlockObject {
  object(value) {
    console.log("image 정보", value);
    return new FileObject().object(value);
  }
  get(value) {
    console.log("image 정보", value);
    return value["image"]["external"]["url"];
  }
}


class LinkPreviewBlockObject {
  object(value) {
    console.log("link_preview 정보", value);
    return {};
  }
  get(value) {
    console.log("link_preview 정보", value);
    return {};
  }
}


class MentionBlockObject {
  object(value) {
    console.log("mention 정보", value);
    return {};
  }
  get(value) {
    console.log("mention 정보", value);
    return {};
  }
}


class NumberedListItemBlockObject {
  object(value) {
    console.log("numbered_list_item 정보", value);
    return {};
  }
  get(value) {
    console.log("numbered_list_item 정보", value);
    return {};
  }
}


class ParagraphBlockObject {
  object(value, { color = "default" } = {}) {
    const result = { "paragraph": new TextObject().object(value) };
    result["paragraph"]["color"] = color;
    return result;
  }
  get(value) {
    return new Heading123BlockObject().get(value);
  }
}


class PDFBlockObject {
  object(value) {
    console.log("pdf 정보", value);
    return new FileObject().object(value);
  }
  get(value) {
    console.log("pdf 정보", value);
    return value["pdf"]["external"]["url"];
  }
}


class QuoteBlockObject {
  object(value) {
    console.log("quote 정보", value);
    return {};
  }
  get(value) {
    console.log("quote 정보", value);
    return {};
  }
}


class SyncedBlockBlockObject {
  object(value) {
    console.log("synced_block 정보", value);
    return {};
  }
  get(value) {
    console.log("synced_block 정보", value);
    return {};
  }
}


class TableBlockObject {
  object(value) {
    console.log("table 정보", value);
    return {};
  }
  get(value) {
    console.log("table 정보", value);
    return {};
  }
}


class ToDoBlockObject {
  object(value) {
    console.log("to_do 정보", value);
    return new TextObject().object(value);
  }
  get(value) {
    console.log("to_do 정보", value);
    return new TextObject().get(value);
  }
}


class ToggleBlocksBlockObject {
  object(value) {
    console.log("toggle 정보", value);
    return new TextObject().object(value);
  }
  get(value) {
    console.log("toggle 정보", value);
    return new Heading123BlockObject().get(value);
  }
}


class VideoBlockObject {
  object(url) {
    console.log("video 정보", url);
    return new FileObject().object(url);
  }
  get(value) {
    console.log("video 정보", value);
    return value["video"]["external"]["url"];
  }
}


// 파이썬의 class BlockObject(ListValueBase) 역할
class BlockObject extends ListValueBase {
  audio(url) {
    const result = new AudioBlockObject().object(url);
    this._value.push(result);
    return this;
  }
  bookmark(value) {
    const result = new BookmarkBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  breadcrumb(value) {
    const result = new BreadcrumbBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  bulleted_list_item(value) {
    const result = new BulletedListItemBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  callout(value, options = {}) {
    const result = new CalloutBlockObject().object(value, options);
    this._value.push(result);
    return this;
  }
  child_database(value) {
    const result = new ChildDatabaseBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  // child_page(value) {
  //   const result = new ChildPageBlockObject().object(value);
  //   this._value.push(result);
  //   return this;
  // }
  code(value) {
    const result = new CodeBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  column(value) {
    const result = new ColumnListAndColumnBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  column_list(value) {
    const result = new ColumnListAndColumnBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  divider(value) {
    const result = new DividerBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  embed(url) {
    const result = new EmbedBlockObject().object(url);
    this._value.push(result);
    return this;
  }
  equation(value) {
    const result = new EquationBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  file(url) {
    const result = new FileBlockObject().object(url);
    this._value.push(result);
    return this;
  }
  heading_1(value) {
    const result = new Heading123BlockObject().object(value);
    this._value.push(result);
    return this;
  }
  heading_2(value) {
    const result = new Heading123BlockObject().object(value);
    this._value.push(result);
    return this;
  }
  heading_3(value) {
    const result = new Heading123BlockObject().object(value);
    this._value.push(result);
    return this;
  }
  image(value) {
    const result = new ImageBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  link_preview(value) {
    const result = new LinkPreviewBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  mention(value) {
    const result = new MentionBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  numbered_list_item(value) {
    const result = new NumberedListItemBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  text(value, options = {}) {
    const result = new ParagraphBlockObject().object(value, options);
    this._value.push(result);
    return this;
  }
  pdf(value) {
    const result = new PDFBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  quote(value) {
    const result = new QuoteBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  synced_block(value) {
    const result = new SyncedBlockBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  table(value) {
    const result = new TableBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  to_do(value) {
    const result = new ToDoBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  toggle(value) {
    const result = new ToggleBlocksBlockObject().object(value);
    this._value.push(result);
    return this;
  }
  video(url) {
    const result = new VideoBlockObject().object(url);
    this._value.push(result);
    return this;
  }
}
//#endregion


//#region 3. 노션 데이터베이스 속성 정의
class CheckboxDatabaseObject {
  object(value) {
    return { "checkbox": value, "type": "checkbox" };
  }
  get(value) {
    return value["checkbox"];
  }
}


class CreatedByDatabaseObject {
  get(value) {
    return value["created_by"]["id"];
  }
}


class CreatedTimeDatabaseObject {
  get(value) {
    return value["created_time"];
  }
}


class DateDatabaseObject {
  /**
   * 날짜 ex) '2022-08-08'
   */
  object(start, end) {
    if (typeof start === 'string') {
      return { "date": { "start": start, "end": end }, "type": "date" };
    } else if (start === null || start === undefined) {
      return { "date": null, "type": "date" };
    }
    return {};
  }
  get(value) {
    if (value["date"] === null || value["date"] === undefined) {
      return null;
    }
    return {
      "start": value["date"]["start"],
      "end": value["date"]["end"]
    };
  }
}


class EmailDatabaseObject {
  object(value) {
    return { "email": value, "type": "email" };
  }
  get(value) {
    return value["email"];
  }
}


class FilesDatabaseObject {
  object(name, url) {
    return {
      "type": "files",
      "files": [
        {
          "name": name,
          "external": { "url": url }
        }
      ]
    };
  }
  get(value) {
    if (!value["files"] || value["files"].length === 0) {
      return null;
    }
    return {
      "name": value["files"][0]["name"],
      "file": value["files"][0]["external"]["url"]
    };
  }
}


class FormulaDatabaseObject {
  // 업데이트 불가능
  get(value) {
    return value["formula"];
  }
}


class LastEditedByDatabaseObject {
  get(value) {
    return value["last_edited_by"]["id"];
  }
}


class LastEditedTimeDatabaseObject {
  get(value) {
    return value["last_edited_time"];
  }
}


class MultiSelectDatabaseObject {
  // 파이썬의 (value: str, *values: str) 구조를 JS Rest 파라미터로 대체
  object(value, ...values) {
    const result = [{ "name": value }];
    result.push(...values.map(v => ({ "name": v })));
    return { "multi_select": result, "type": "multi_select" };
  }
  get(value) {
    if (!value["multi_select"] || value["multi_select"].length === 0) {
      return [];
    }
    return value["multi_select"].map(select => select["name"]);
  }
}


class NumberDatabaseObject {
  object(value) {
    return { "number": value, "type": "number" };
  }
  get(value) {
    return value["number"];
  }
}


class PeopleDatabaseObject {
  object(id, ...ids) {
    const result = [{ "id": id }];
    result.push(...ids.map(peopleId => ({ "id": peopleId })));
    return { "people": result, "type": "people" };
  }
  get(value) {
    if (!value["people"] || value["people"].length === 0) {
      return [];
    }
    return value["people"].map(people => people["name"]);
  }
}


class PhoneNumberDatabaseObject {
  object(value) {
    return { "phone_number": value, "type": "phone_number" };
  }
  get(value) {
    return value["phone_number"];
  }
}


class PlaceDatabaseObject {
  get(value) {
    if (value["place"] === null || value["place"] === undefined) {
      return null;
    }
    return {
      "lat": value["place"]["lat"],
      "lon": value["place"]["lon"],
      "name": value["place"]["name"],
      "address": value["place"]["address"],
    };
  }
}


class RelationDatabaseObject {
  object(id, ...ids) {
    const result = [{ "id": id }];
    result.push(...ids.map(relationId => ({ "id": relationId })));
    return { "relation": result, "type": "relation" };
  }
  get(value) {
    if (!value["relation"] || value["relation"].length === 0) {
      return null;
    }
    // value["relation"] 안에 { "id": "..." } 밖에 없음
    return value["relation"].map(relation => relation["id"]);
  }
}


class RichTextDatabaseObject {
  object(value) {
    if (typeof value === 'string') {
      return { "rich_text": [ { "text": { "content": value }, "type": "text" } ] };
    } else if (value === null || value === undefined) {
      return { "rich_text": [] };
    }
    return {};
  }
  get(value) {
    const type_ = value["type"];
    if (!value[type_] || value[type_].length === 0) {
      return null;
    }
    return value[type_][0]["plain_text"];
  }
}


class RollupDatabaseObject {
  get(value) {
    const array = value["rollup"]["array"];
    if (!array || array.length === 0) {
      return null;
    }
    const type_ = array[0]["type"];
    return parser_database_object_data(type_, array[0]);
  }
}


class SelectDatabaseObject {
  object(value) {
    if (typeof value === 'string') {
      return { "select": { "name": value }, "type": "select" };
    } else if (value === null || value === undefined) {
      return { "select": null };
    }
    return {};
  }
  get(value) {
    if (value["select"] === null || value["select"] === undefined) {
      return null;
    }
    return value["select"]["name"];
  }
}


class StatusDatabaseObject {
  object(value) {
    return { "status": { "name": value }, "type": "status" };
  }
  get(value) {
    // 항상 값이 존재 (기본값이 있음)
    return value["status"]["name"];
  }
}


class TitleDatabaseObject {
  object(value) {
    if (typeof value === 'string') {
      return { "title": [ { "text": { "content": value }, "type": "text" } ], "type": "title" };
    } else if (value === null || value === undefined) {
      return { "title": [], "type": "title" };
    }
    return {};
  }
  get(value) {
    if (!value["title"] || value["title"].length === 0) {
      return null;
    }
    return value["title"][0]["plain_text"];
  }
}


class UrlDatabaseObject {
  /**
   * URL
   */
  object(value) {
    return { "url": value, "type": "url" };
  }
  get(value) {
    return value["url"];
  }
}


class UniqueIDDatabaseObject {
  get(value) {
    return value["unique_id"]["number"];
  }
}


class ButtonDatabaseObject {
  get(value) {
    return value["button"];
  }
}


class DatabaseObject extends DictValueBase {
  /** 체크박스가 선택되었는지(True) 또는 선택되지 않았는지(False)를 나타냅니다. */
  checkbox(properties, value) {
    this._value[properties] = new CheckboxDatabaseObject().object(value);
    return this;
  }

  /**
   * 페이지 속성 값의 가 인 경우 , 해당 속성 값에는 다음과 같은 필드를 가진 객체가 포함됩니다.
   * 
   * 예시값 "2020-12-08T12:00:00Z", "2020-12-08T12:00:00Z”
   */
  date(properties, start, end = null) {
    this._value[properties] = new DateDatabaseObject().object(start, end);
    return this;
  }

  /** 이메일 주소를 설명하는 문자열입니다. */
  email(properties, value) {
    this._value[properties] = new EmailDatabaseObject().object(value);
    return this;
  }

  /** 파일에 대한 정보를 담고 파일 이름과 url */
  files(properties, name, url) {
    this._value[properties] = new FilesDatabaseObject().object(name, url);
    return this;
  }

  /** 표시되는 옵션 이름입니다 */
  multi_select(properties, value, ...values) {
    this._value[properties] = new MultiSelectDatabaseObject().object(value, ...values);
    return this;
  }

  /** 어떤 값을 나타내는 숫자. */
  number(properties, value) {
    this._value[properties] = new NumberDatabaseObject().object(value);
    return this;
  }

  /** 유저의 id 값을 넣으면 되긴 한데 구하기 쉽지 않음 */
  people(properties, id, ...ids) {
    this._value[properties] = new PeopleDatabaseObject().object(id, ...ids);
    return this;
  }

  /** 전화번호를 나타내는 문자열입니다. 전화번호 형식은 지정되어 있지 않습니다. */
  phone_number(properties, value) {
    this._value[properties] = new PhoneNumberDatabaseObject().object(value);
    return this;
  }

  /** 다른 데이터베이스의 페이지 id 값을 넣어주면 됨 */
  relation(properties, id, ...ids) {
    this._value[properties] = new RelationDatabaseObject().object(id, ...ids);
    return this;
  }

  /** 텍스트 */
  text(properties, value) {
    this._value[properties] = new RichTextDatabaseObject().object(value);
    return this;
  }

  /** 표시되는 옵션 이름입니다 */
  select(properties, value) {
    this._value[properties] = new SelectDatabaseObject().object(value);
    return this;
  }

  /** 표시되는 옵션 이름입니다 */
  status(properties, value) {
    this._value[properties] = new StatusDatabaseObject().object(value);
    return this;
  }

  /** 타이틀 */
  title(properties, value) {
    this._value[properties] = new TitleDatabaseObject().object(value);
    return this;
  }

  /** 웹 주소를 설명하는 문자열입니다. */
  url(properties, value) {
    this._value[properties] = new UrlDatabaseObject().object(value);
    return this;
  }

  /** children */
  children(blockObject) {
    if (blockObject instanceof BlockObject) {
      this._value["children"] = blockObject.value;
    } else {
      this._value["children"] = blockObject;
    }
    return this;
  }
}


// 파이썬의 match-case 분기 함수 역할
function parser_database_object_data(type_, data) {
  switch (type_) {
    case "checkbox":
      return new CheckboxDatabaseObject().get(data);
    case "created_by":
      return new CreatedByDatabaseObject().get(data);
    case "created_time":
      return new CreatedTimeDatabaseObject().get(data);
    case "date":
      return new DateDatabaseObject().get(data);
    case "email":
      return new EmailDatabaseObject().get(data);
    case "files":
      return new FilesDatabaseObject().get(data);
    case "formula":
      return new FormulaDatabaseObject().get(data);
    case "last_edited_by":
      return new LastEditedByDatabaseObject().get(data);
    case "last_edited_time":
      return new LastEditedTimeDatabaseObject().get(data);
    case "multi_select":
      return new MultiSelectDatabaseObject().get(data);
    case "number":
      return new NumberDatabaseObject().get(data);
    case "people":
      return new PeopleDatabaseObject().get(data);
    case "phone_number":
      return new PhoneNumberDatabaseObject().get(data);
    case "place":
      return new PlaceDatabaseObject().get(data);
    case "relation":
      return new RelationDatabaseObject().get(data);
    case "rich_text":
      return new RichTextDatabaseObject().get(data);
    case "rollup":
      return new RollupDatabaseObject().get(data);
    case "select":
      return new SelectDatabaseObject().get(data);
    case "status":
      return new StatusDatabaseObject().get(data);
    case "title":
      return new TitleDatabaseObject().get(data);
    case "url":
      return new UrlDatabaseObject().get(data);
    case "unique_id":
      return new UniqueIDDatabaseObject().get(data);
    case "button":
      return new ButtonDatabaseObject().get(data);
    default:
      console.log(`이건 무슨 타입?: ${type_}`);
      console.log(`이건 그래서?:`, data);
      return {};
  }
}
//#endregion


//#region 4. 필터 및 정렬 빌더 정의
// 헬퍼 함수: 파이썬의 _return_value 역할
function _returnValue(property_, filterName, field, value) {
  return {
    "property": property_,
    [filterName]: { [field]: value }
  };
}


// 헬퍼 함수: 카멜 케이스를 스네이크 케이스로 변환 (CheckboxFilter -> checkbox)
function _camelToSnake(name) {
  const s1 = name.replace(/(.)([A-Z][a-z]+)/g, '$1_$2');
  return s1.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase();
}


// 부모 필터 클래스
class FilterBase extends DictValueBase {
  constructor(value = null) {
    super(value);
    const className = this.constructor.name.replace("Filter", "");
    this._filterName = _camelToSnake(className);
  }
}


// 수식 필터 타입 매칭용 베이스 클래스들
// 타입 확인 해야지 ...
class CheckboxFilterBase extends FilterBase {}
class DateFilterBase extends FilterBase {}
class NumberFilterBase extends FilterBase {}
class RichTextFilterBase extends FilterBase {}


class CheckboxFilter extends FilterBase {
  /** 속성 값이 제공된 값과 정확히 일치하는지 여부를 나타냅니다.
   * 
   * 값이 정확히 일치하는 모든 데이터 소스 항목을 반환하거나 제외합니다.
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new CheckboxFilterBase(this._value);
  }
  /** 속성 값이 제공된 값과 다른지 여부를 나타냅니다.
   * 
   * 값에 차이가 있는 모든 데이터 소스 항목을 반환하거나 제외합니다.
   */
  does_not_equal(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_equal", value);
    Object.assign(this._value, result);
    return new CheckboxFilterBase(this._value);
  }
}


class DateFilter extends FilterBase {
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값이 제공된 날짜 이후인 데이터 소스 항목을 반환합니다.
   * 
   * ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00"
   */
  after(property_, value) {
    const result = _returnValue(property_, this._filterName, "after", value);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값이 제공된 날짜 이전인 데이터 소스 항목을 반환합니다.
   * 
   * ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00"
   */
  before(property_, value) {
    const result = _returnValue(property_, this._filterName, "before", value);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값이 제공된 날짜인 데이터 소스 항목을 반환합니다.
   * 
   * ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00"
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값이 다음 달 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  next_month(property_) {
    const result = _returnValue(property_, this._filterName, "next_month", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값이 다음 주 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  next_week(property_) {
    const result = _returnValue(property_, this._filterName, "next_week", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값이 내년 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  next_year(property_) {
    const result = _returnValue(property_, this._filterName, "next_year", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값이 지정된 날짜와 같거나 이후인 데이터 소스 항목을 반환합니다.
   * 
   * ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00"
   */
  on_or_after(property_, value) {
    const result = _returnValue(property_, this._filterName, "on_or_after", value);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 날짜 속성 값과 비교할 값입니다.
   * 
   * 날짜 속성 값이 지정된 날짜와 같거나 이전인 데이터 소스 항목을 반환합니다.
   * 
   * ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00"
   */
  on_or_before(property_, value) {
    const result = _returnValue(property_, this._filterName, "on_or_before", value);
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 지난달 이내의 부동산 가치가 있는 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  past_month(property_) {
    const result = _returnValue(property_, this._filterName, "past_month", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 지난주 이내의 속성 값이 포함된 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  past_week(property_) {
    const result = _returnValue(property_, this._filterName, "past_week", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 해당 속성 가치가 지난 1년 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  past_year(property_) {
    const result = _returnValue(property_, this._filterName, "past_year", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
  /** 이번 주에 속성 값이 있는 데이터 소스 항목으로 결과를 제한하는 필터입니다. */
  this_week(property_) {
    const result = _returnValue(property_, this._filterName, "this_week", {});
    Object.assign(this._value, result);
    return new DateFilterBase(this._value);
  }
}


class FilesFilter extends FilterBase {
  /** 파일 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.
   * 
   * 속성 값이 비어 있는 모든 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.
   * 
   * 속성 값 이 채워진 모든 항목을 반환합니다
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class FormulaFilter extends FilterBase {
  /** 수식 결과를 비교할 체크박스 필터 조건입니다.
   * 
   * 수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다.
   */
  checkbox(property_, value) {
    const _val = value.value["checkbox"];
    const result = _returnValue(property_, this._filterName, "checkbox", _val);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 수식 결과를 비교할 날짜 필터 조건입니다.
   * 
   * 수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다.
   */
  date(property_, value) {
    const _val = value.value["date"];
    const result = _returnValue(property_, this._filterName, "date", _val);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 수식 결과를 비교할 숫자 필터 조건입니다.
   * 
   * 수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다.
   */
  number(property_, value) {
    const _val = value.value["number"];
    const result = _returnValue(property_, this._filterName, "number", _val);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 수식 결과를 비교할 서식 있는 텍스트 필터 조건입니다.
   * 
   * 수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다.
   */
  string(property_, value) {
    const _val = value.value["rich_text"];
    const result = _returnValue(property_, this._filterName, "string", _val);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class MultiSelectFilter extends FilterBase {
  /** 다중 선택 속성 값을 비교할 값입니다.
   * 
   * 다중 선택 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다.
   */
  contains(property_, value) {
    const result = _returnValue(property_, this._filterName, "contains", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 다중 선택 속성 값을 비교할 값입니다.
   * 
   * 다중 선택 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다.
   */
  does_not_contain(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_contain", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 다중 선택 속성 값이 비어 있는지 여부를 나타냅니다.
   * 
   * 다중 선택 값에 데이터가 없는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 다중 선택 속성 값이 비어 있지 않은지 여부를 나타냅니다.
   * 
   * 다중 선택 값에 데이터가 포함된 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class NumberFilter extends FilterBase {
  /** 숫자 속성 값을 비교할 입니다.
   * 
   * 숫자 속성 값이 제공된 값과 다른 데이터 소스 항목을 반환합니다.
   */
  does_not_equal(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_equal", value);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 숫자 속성 값을 비교할 대상입니다.
   * 
   * 숫자 속성 값이 제공된 숫자와 동일한 데이터 소스 항목을 반환합니다.
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 숫자 속성 값을 비교할 대상입니다.
   * 
   * 숫자 속성 값이 제공된 값을 초과하는 데이터 소스 항목을 반환합니다.
   */
  greater_than(property_, value) {
    const result = _returnValue(property_, this._filterName, "greater_than", value);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 숫자 속성 값을 비교할 대상입니다.
   * 
   * 숫자 속성 값이 제공된 값보다 크거나 같은 데이터 소스 항목을 반환합니다.
   */
  greater_than_or_equal_to(property_, value) {
    const result = _returnValue(property_, this._filterName, "greater_than_or_equal_to", value);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 속성 값이 비어 있는지 여부를 나타냅니다.
   * 
   * 숫자 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 숫자 속성 값이 비어 있는지 여부를 나타냅니다.
   * 
   * 숫자 속성 값에 데이터가 포함된 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 숫자 속성 값을 비교할 대상입니다.
   * 
   * 숫자 속성 값이 제공된 값보다 작은 데이터 소스 항목을 반환합니다.
   */
  less_than(property_, value) {
    const result = _returnValue(property_, this._filterName, "less_than", value);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
  /** 숫자 속성 값을 비교할 대상입니다.
   * 
   * 숫자 속성 값이 제공된 값보다 작거나 같은 데이터 소스 항목을 반환합니다.
   */
  less_than_or_equal_to(property_, value) {
    const result = _returnValue(property_, this._filterName, "less_than_or_equal_to", value);
    Object.assign(this._value, result);
    return new NumberFilterBase(this._value);
  }
}


class PeopleFilter extends FilterBase {
  /** people 속성 값과 비교할 값입니다.
   * 
   * people 속성 값에 제공된 사람이 포함된 데이터 소스 항목을 반환합니다.
   */
  contains(property_, value) {
    const result = _returnValue(property_, this._filterName, "contains", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** people 속성 값과 비교할 값입니다.
   * 
   * people 속성 값에 제공된 사람이 포함되지 않은 데이터 소스 항목을 반환합니다.
   */
  does_not_contain(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_contain", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** people 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.
   * 
   * people 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** people 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.
   * 
   * people 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class RelationFilter extends FilterBase {
  /** 관계 속성 값과 비교할 값입니다.
   * 
   * 관계 속성 값에 제공된 페이지가 포함된 데이터 소스 항목을 반환합니다.
   */
  contains(property_, value) {
    const result = _returnValue(property_, this._filterName, "contains", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 관계 속성 값과 비교할 값입니다.
   * 
   * 관계 속성 값에 제공된 페이지가 포함되지 않은 데이터 소스 항목을 반환합니다.
   */
  does_not_contain(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_contain", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 관계 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.
   * 
   * 관계 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 관계 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.
   * 
   * 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class RichTextFilter extends FilterBase {
  /** 텍스트 속성 값을 비교할 대상입니다.
   * 
   * 제공된 값을 포함하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다.
   */
  contains(property_, value) {
    const result = _returnValue(property_, this._filterName, "contains", value);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값을 비교할 대상입니다.
   * 
   * 제공된 값을 포함하지 않는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다.
   */
  does_not_contain(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_contain", value);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값을 비교할 대상입니다.
   * 
   * 제공된 값과 일치하지 않는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다.
   */
  does_not_equal(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_equal", value);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값을 비교할 대상입니다.
   * 
   * 제공된 값으로 끝나는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다.
   */
  ends_with(property_, value) {
    const result = _returnValue(property_, this._filterName, "ends_with", value);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값을 비교할 대상입니다.
   * 
   * 제공된 값과 일치하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.
   * 
   * 텍스트 속성 값이 비어 있는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.
   * 
   * 데이터가 포함된 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
  /** 텍스트 속성 값을 비교할 대상입니다. 제공된 값으로 시작하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다. */
  starts_with(property_, value) {
    const result = _returnValue(property_, this._filterName, "starts_with", value);
    Object.assign(this._value, result);
    return new RichTextFilterBase(this._value);
  }
}


// class RollupFilter extends FilterBase { ... // 일단 패스


class SelectFilter extends FilterBase {
  /** select 속성 값을 비교할 대상입니다.
   * 
   * select 속성 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다.
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** select 속성 값을 비교할 대상입니다.
   * 
   * select 속성 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다.
   */
  does_not_equal(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_equal", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** select 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.
   * 
   * select 속성 값이 비어 있는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** select 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.
   * 
   * select 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class StatusFilter extends FilterBase {
  /** 상태 속성 값을 비교할 문자열입니다.
   * 
   * 상태 속성 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다.
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 상태 속성 값을 비교할 문자열입니다.
   * 
   * 상태 속성 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다.
   */
  does_not_equal(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_equal", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 상태 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.
   * 
   * 상태 속성 값이 비어 있는 데이터 소스 항목을 반환합니다.
   */
  is_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** 상태 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.
   * 
   * 상태 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다.
   */
  is_not_empty(property_) {
    const result = _returnValue(property_, this._filterName, "is_not_empty", true);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


// class TimestampFilter extends FilterBase { ...
// 얘 혼자 이상함 남들 전부 property 쓸 때 얘는 timestamp 씀
// {
//   "filter": {
//     "timestamp": "created_time",
//     "created_time": {
//       "on_or_before": "2022-10-13"
//     }
//   }
// }


class VerificationFilter extends FilterBase {
  /** 쿼리 중인 확인 상태입니다. 유효한 옵션은 다음과 같습니다.
   * 
   * "verified", "expired", null 현재 확인 상태가 쿼리된 상태와 일치하는 데이터 소스 항목을 반환합니다.
   */
  status(property_, value) {
    const result = _returnValue(property_, this._filterName, "status", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


class IDFilter extends FilterBase {
  /** unique_id 속성 값과 비교할 값입니다.
   * 
   * unique_id 속성 값이 제공된 값과 다른 데이터 소스 항목을 반환합니다.
   */
  does_not_equal(property_, value) {
    const result = _returnValue(property_, this._filterName, "does_not_equal", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** unique_id 속성 값과 비교할 값입니다.
   * 
   * unique_id 속성 값이 제공된 값과 동일한 데이터 소스 항목을 반환합니다.
   */
  equals(property_, value) {
    const result = _returnValue(property_, this._filterName, "equals", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** unique_id 속성 값과 비교할 값입니다.
   * 
   * unique_id 속성 값이 제공된 값을 초과하는 데이터 소스 항목을 반환합니다.
   */
  greater_than(property_, value) {
    const result = _returnValue(property_, this._filterName, "greater_than", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** unique_id 속성 값과 비교할 값입니다.
   * 
   * unique_id 속성 값이 제공된 값과 같거나 큰 데이터 소스 항목을 반환합니다.
   */
  greater_than_or_equal_to(property_, value) {
    const result = _returnValue(property_, this._filterName, "greater_than_or_equal_to", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** unique_id 속성 값과 비교할 값입니다.
   * 
   * unique_id 속성 값이 제공된 값보다 작은 데이터 소스 항목을 반환합니다.
   */
  less_than(property_, value) {
    const result = _returnValue(property_, this._filterName, "less_than", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
  /** unique_id 속성 값과 비교할 값입니다.
   * 
   * unique_id 속성 값이 제공된 값보다 작거나 같은 데이터 소스 항목을 반환합니다.
   */
  less_than_or_equal_to(property_, value) {
    const result = _returnValue(property_, this._filterName, "less_than_or_equal_to", value);
    Object.assign(this._value, result);
    return new FilterBase(this._value);
  }
}


// 최종 엔트리포인트 Filter 클래스 및 복합 조건(and, or) 처리
class Filter extends FilterBase {
  static checkbox = new CheckboxFilter();
  static date = new DateFilter();
  static files = new FilesFilter();
  static formula = new FormulaFilter();
  static multi_select = new MultiSelectFilter();
  static number = new NumberFilter();
  static people = new PeopleFilter();
  static relation = new RelationFilter();
  static text = new RichTextFilter();
  // static rollu = RollupFilter()
  static select = new SelectFilter();
  static status = new StatusFilter();
  // static timestamp = Timestamp()
  static verification = new VerificationFilter();
  static id = new IDFilter();

  static and_(filter_, ...filters) {
    const filterList = [filter_.value, ...filters.map(f => f.value)];
    return new Filter({ "and": filterList });
  }

  static or_(filter_, ...filters) {
    const filterList = [filter_.value, ...filters.map(f => f.value)];
    return new Filter({ "or": filterList });
  }
}


// 정렬(Sort) 클래스들
class SortBase extends ListValueBase {}

class Sort extends SortBase {
  static sort(property_, direction) {
    const result = { "property": property_, "direction": direction };
    return new _Sort([result]);
  }
}

class _Sort extends SortBase {
  sort(property_, direction) {
    const result = { "property": property_, "direction": direction };
    this._value.push(result);
    return this;
  }
}
//#endregion


//#region 5. 핵심 API 실행 클라이언트 정의
class NotionDatabasePage extends NotionBase {
  constructor(apiKey, id, object, values, types) {
    super(apiKey, id, object);
    this._values = values;
    this._types = types;
  }

  // 데이터 수정 (PATCH)
  async update(updatePropertiesObject) {
    const url = `https://api.notion.com/v1/pages/${this.id}`;
    const headers = this._addHeaders("2025-09-03");
    const updateProperties = updatePropertiesObject.value;

    const payload = {
      "in_trash": false,
      "erase_content": false,
      "properties": updateProperties
    };

    const response = await fetch(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(JSON.stringify(await response.json()));
    }

    const responseData = await response.json();
    const newPage = _parserPage(this.apiKey, responseData);
    
    // 상태 동기화
    this._values = newPage._values;
    this._types = newPage._types;
    return newPage;
  }

  // 데이터 휴지통 이동 (PATCH)
  async remove() {
    const url = `https://api.notion.com/v1/pages/${this.id}`;
    const headers = this._addHeaders("2025-09-03");
    const payload = { "archived": true }; // 원본 파이썬 로직 유지
    // 삭제는 archived 를 true 로, 되살리고 싶다면 archived 를 false 로

    const response = await fetch(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error(`오류가 남: ${response.json()}`);
    }

    const responseData = await response.json();
    return responseData;
  }

  get value() {
    return this._values;
  }

  // 자바스크립트의 __str__ 역할 (객체를 문자열로 표현할 때 사용)
  toString() {
    if (this.archived) {
      return "{페이지: 삭제됨}";
    }
    const entries = Object.entries(this._values);
    const result = entries.map(([key, value]) => `${key}=${value}`);
    if (3 < result.length) {
      return `{페이지: ${result.slice(0, 3).join(",")} ...}`;
    }
    return `{페이지: ${result.join(",")}}`;
  }
}

// 응답받은 페이지 데이터를 파싱하는 독립 헬퍼 함수
function _parserPage(apiKey, data) {
  const id = data["id"];
  const object = data["object"];
  const values = {};
  const types = {};
  const properties = data["properties"] || {};

  for (const [key, value] of Object.entries(properties)) {
    const type = value["type"];
    values[key] = parser_database_object_data(type, value);
    types[key] = type;
  }
  return new NotionDatabasePage(apiKey, id, object, values, types);
}


class NotionDatabaseLite extends NotionBase {
  constructor(key, DB_id) {
    super(key, DB_id, "database");
    this._datas = [];
  }

  // 데이터 추가 (POST)
  async write(writePropertiesObject) {
    const url = "https://api.notion.com/v1/pages";
    const headers = this._addHeaders("2022-06-28");

    let properties = writePropertiesObject;
    if (writePropertiesObject instanceof DatabaseObject) {
      properties = writePropertiesObject.value;
    }

    const payload = {
      "parent": { "database_id": this.id },
      "properties": properties
    };

    // children이 있다면 추출 후 payload의 최상위로 이동
    if ("children" in properties) {
      const children = properties["children"];
      delete properties["children"];
      payload["children"] = children;
    }

    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(JSON.stringify(await response.json()));
    }

    const responseData = await response.json();
    const newPage = _parserPage(this.api_key, responseData);
    this._datas.push(newPage);
    return newPage;
  }

  // 데이터 쿼리 조회 (POST)
  async read({ filter = null, sort = null, page_size = 100 } = {}) {
    const url = `https://api.notion.com/v1/databases/${this.id}/query`;
    const headers = this._addHeaders("2022-06-28");

    const payload = {};
    payload["page_size"] = Math.max(0, Math.min(page_size, 100));

    if (filter !== null) {
      payload["filter"] = filter instanceof FilterBase ? filter.value : filter;
    }
    if (sort !== null) {
      payload["sorts"] = sort instanceof SortBase ? sort.value : sort;
    }

    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(JSON.stringify(await response.json()));
    }

    const responseData = await response.json();
    this._datas = this._parse(responseData);
  }

  // 수정 (인덱스 숫자 또는 오브젝트 직접 받기)
  async update(pageOrIndex, updatePropertiesObject) {
    let obj;
    if (typeof pageOrIndex === 'number') {
      obj = this.value[pageOrIndex];
    } else {
      obj = pageOrIndex;
    }
    await obj.update(updatePropertiesObject);
  }

  // 삭제 (인덱스 숫자 또는 오브젝트 직접 받기)
  async remove(pageOrIndex) {
    let obj;
    if (typeof pageOrIndex === 'number') {
      obj = this.value[pageOrIndex];
    } else {
      obj = pageOrIndex;
    }
    return await obj.remove();
  }

  _parse(responseData) {
    const results = responseData["results"] || [];
    return results.map(data => _parserPage(this.apiKey, data));
  }

  get value() {
    return this._datas;
  }

  toString() {
    const dataSourcesCount = this._datas.length;
    if (dataSourcesCount === 0) {
      return "데이터베이스: 데이터 소스 없음";
    }

    const stringList = this._datas.map(source => source.toString());
    if (3 < dataSourcesCount) {
      return `[데이터베이스: ${stringList.slice(0, 3).join(",")}...]`;
    }
    return `[데이터베이스: ${stringList.join(",")}]`;
  }
}
//#endregion

