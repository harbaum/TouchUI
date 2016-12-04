# TouchUI Web Interface

This document describes a web interface for querying and controlling the TouchUI launcher and the applications launched by the launcher. This web interface is intended as a replacement and extension of the existing TCP control interface as implemented by TouchUI today.

The TouchUI web interface provides access to the following functions:

* Display messages and/or ask for user confirmation (this corresponds to the TCPServer "msg" and "confirm" commands)
* List all apps known to the launcher
* Query and set metadata of a given existing app (app metadata is stored in the manifest of the app)
* Read and write files belonging to an existing app
* create a new app
* check which (if any) app is currently running
* stop a running app
* launch an existing app and (optionally) interact with this app

Most of these functions are implemented as a (mostly) RESTful HTTP interface, with the sole exception of launching and interacting with an existing app, which is implemented unsing the Websocket protocol.

If not explicitly mentioned, all functions use the canonical HTTP status codes `200 (OK)` to indicate success and `500 (server error)` to indicate failure.

## Display a launcher message or a confirmation dialog

Both launcher messages and confirmation dialogs can be displayed by sending a HTTP POST request to the `/message` URI. The request body must have the content type `application/x-www-form-urlencoded`, and may contain the following keys:

* `message`: The message to display. This key must be present, if it is missing, the request will fail with a HTTP status code of `400 (bad request)`
* `confirm`: Optional. If present, the launcher will display a confirmation dialog instead of a simple message window, and send the value from this key in the response body if the user presses the *Confirm* button.
* `cancel`: Optional. If present, the launcher will display a confirmation dialog instead of a simple message window, and send the value from this key in the response body if the user presses the *Cancel* button.

The response body of a `/message` request has the context type `text/plain; encoding=utf-8` and contains the `confirm` or `cancel` value corresponding to the users choice for a confirmation dialog. For a simple message, the response body is empty.

Note: A confirmation dialog will wait for user intercation via touch screen before returning a response. This may lead to timeouts on the client side.

## List launcher apps

A list of all apps known to the launcher can be retrieved by sending a HTTP GET request to `/app/index`. The response has content type `application/json` and contains a JSON array. The individual entries in this array are JSON representations of the manifest for each app known to the launcher.

## Read and write app files

Files belonging to an existing app can be read by sending an HTTP GET request to `/app/${uuid}/${filename}`, where `${uuid}` is the UUID of an existing app (as specified in the app manifest) and `${filename}` is the name of a file in the app directory. The response is either the HTTP status code `200 (OK)` with the requested file as the response body (the content type depends on the file contents in this case), or the HTTP status code `404 (not found)` with an empty response body.

Files belonging to an existing app can be replaced by sending an HTTP PUT request to `/app/${uuid}/${filename}`, where `${uuid}` and `${filename}` are defined as above. The response is either the HTTP status code `200 (OK)` if the file has been replaced sucessfully, or the HTTP status code `404 (not found)`. In either case, the response body is empty.

## Create a new app

To be specified later.

## Query which app is currently running.

The currently running app &mdash; if any &mdash; can be queried by sending an HTTP GET request to `/app/control`. The response body has the content type `application/json` and contains either JSON object of the form (`{"success":true}`) if no app is currently running or a JSON object of the form `{"success":true,"running":"${uuid}"}`, where `${uuid}` is the UUID of the app currently running.

## Stop a running app

The currently running app can be stopped by sending an HTTP POST request to `/app/control`. The request body must have the content type `application/json`, and the request body must contain a JSON object of the form `{"stop":"${uuid}"}`, where `${uuid}` is the UUID of the currently running app. The response body has the same basic format as the response returned by a GET request to `/app/control`, and it reflects the new state. The difference is in the value of the `"success"` field which may be `false` if the launcher could not stop the app as requested (e.g. because no app was running, or because the running app has a different UUID as the app from the "stop" request).

## Launch an app without further interaction

An existing app can be launched by sending an HTTP POST request to `/app/control`. The request body must have the content type `application/json`, and the request body must contain a JSON object of the form `{"launch":"${uuid}"}`, where `${uuid}` is the UUID of an existing app. The response body has the same format as that returned from the "stop" request, and it contains 

Note: A client cannot interact with an app launched by this method. See below on how to launch an app with further interaction.

## Prepare for further interaction with an app

An existing app can be prepared for further interacation by creating a websocket connection to `/app/control/${uuid}`, where `${uuid}` is the UUID of an existing app. 

If the connection attempt is not successful, the launcher replies with an appropriate HTTP status code and an empty response body. In particular, the launcher replies with status code `409 (Conflict)` if another client already has a websocket connection for the specified app, and with `426 (Upgrade required)` (along with the appropriate `Connection` and `Upgrade` headers) if the request is a plain HTTP GET request instead of a Websockets reqeust.

If the connection attempt is successful, the launcher replies by completing the Websocket handshake and listens for messages from the client. The remainder of this document specifies the message format and the set of messages implemented by the launcher.

### Websocket protocol format

All messages on the websocket connection are in JSON format (and UTF-8 encoding). Each message is a single JSON object (as opposed to a JSON array), and all messages share a common set of generic keys:

* `chan`: The message *channel*. May be one of `control`, `io` or `debug`. Not all channels are supported for all apps (in particular, the `debug` channel is only supported by some apps). The only channel that is always supported is the `control` channel.
* `type`: The message *type* within its channel.
* `id`: Optional. An arbitrary string that can be used to associated messages with replies. If a message has an ID, the ID should be unique.
* `re`: Optional. The ID of the message that triggered a reply. The launcher will include a `re` key (and the appropriate value) in every reply to a message which has an `id`.

Individual message types typically define additional message keys.

#### The "control" channel

The control channel provides a superset of the functionality as the `/app/control` REST API. The message types on the control channel are:

* `status`: If sent from the client to the launcher, requests a status reply from the launcher. If sent from the launcher to the client, either a status reply or a reaction to an external event.
* `launch`: Start the app. Semantics are the same as for starting an app using the REST API, and the launcher will reply with the appropriate `status` reply.
* `stop`: Stop the app. Semantics are the same as for stopping an app using the REST API, and the launcher will reply with the appropriate `status` reply.
* `subscribe`: Change the channel subscription. The list of channels to subscribe to is sent as an array of strings under the `channels` key. The launcher will only send (and react to) messages on the subscribed channels. Note: A client cannot unsubscribe from the `control` channel. The control channel is always active.

The most complicated message type on the control channel ist the `status` message as sent from the launcher to the client. Depending on the context, the `status` message will contain additional keys:
* as a reply to a `status` query from the client:
    * `channels`: An array of strings denoting the channels supported for this app.
    * `running`: A string with the UUID of the currently running app. Note that this can be a different app as the one controlled by this websocket connection. This key is only included if an app is running.
* as a reply to a `launch` or `stop` message:
    * `success`: `true` or `false` to indicate the success of the command
    * `running`: A string with the UUID of the currently running app. Note that this can be a different app as the one controlled by this websocket connection. This key is only included if an app is running.
* as a reply to a `subscribe` query from the client:
    * `channels`: An array of strings denoting the currently subscribed channels. Note that this array always includes the value `"control"` for the control channel.
* as a reaction to an external event:
    * `event`: A string denoting the external event. At the moment, this can be only `"launched"` or `"stopped"`, indicating a successfull launch/stop of the app either directly via the launcher GUI or via the REST API.

#### The "io" channel

The io channel allows access to the canonical I/O streams of the app. The message types on the io channel are `stdin`, `stdout` and `stderr`, and all messages have an additional `msg` key with a string value.

The launcher sends a `stdout` or `stderr` message for every line that the app writes to STDOUT or STDERR, with `msg` set to the line written by the app. Note that the trailing `\n` (newline) character will not be included in the message.

Each `stdin` message sent by the client to the launcher is forwarded to the app on STDIN, followed by a `\n` (newline) character.

#### The "debug" channel

The debug channel implements a (simple) debug interface that currently allows setting and clearing of breakpoints, notification about breakpoint hits, and resuming app execution after a breakpoint hit. The debug channel might by extended to a full remote debugger interface later on. An app is not required to support the debug channel.

Currently, all messages on the debug channel have the type `breakpoint`, and have at least the additional key `action`. Possible actions are:

* `status`: If sent from the client to the launcher, request a list of all breakpoints that are currently set. If sent from the launcher to the client, send the current breakpoint list as an array of JSON objects under the additional key `breakpoints` (see below for the format of the objects in this array).
* `set`: Only used by the client. Request that the launcher sets all breakpoints specified in the `breakpoints` array. The launcher replies with a `status` message reflecting the new state.
* `clear`: Only used by the client. Request that the launcher clears all breakpoints specified in the `breakpoints` array (or *all* breakpoints, if no `breakpoints` array is included in the message). The launcher replies with a `status` message reflecting the new state.
* `hit`: Only used by the launcher. Indicates that execution has stopped on a breakpoint. The ID of the breakpoint that has been hit is included under the `breakpoint` key, and the additional key `thread` contains a string that identfies which thread has been stopped.
* `resume`: Only used by the client. Indicates that execution should be resumed for some or all stopped threads. The message may include an array of breakpoint IDs to resume under the `breakpoints` key, and an array of thread IDs to resume as `threads`. Ommitting `breakpoints` or `threads` means "all", and in particular ommitting both means "resume all stopped threads at all breakpoints". The server does not respond to this message.

A single breakpoint is described by a JSON object with these keys:

* `id`: A string, used as a (unique) identifier for this breakpoint. Required.
* `file` and `line`: File name and line number describing the soirce location within the app where the breakpoint should be set. Only required for the breakpoint definitions in a `set` action, but the launcher will include this information in the replies to a `status`, `set` or `clear` action.
* `active`: `true` or `false` depending on wheter the breakpoint is active or not. Defaults to `true` if not set. This value is only explicitly set in launcher responses to a `set` or `clear` action.
