
--boundary_.oOo._WgjNqziM8/n9h+MJ1oxF2TyMBp3V3GZh
Content-Length: 566
Content-Type: application/octet-stream
X-File-MD5: 2859314a3423d476507ef52959213e41
X-File-Mtime: 1718942721
X-File-Path: /DiamondsBucket/CODING/Python-tools/Recompra/.web/utils/helpers/throttle.js

const in_throttle = {};

/**
 * Generic throttle helper
 *
 * @param {string} name - the name of the event to throttle
 * @param {number} limit - time in milliseconds between events
 * @returns true if the event is allowed to execute, false if it is throttled
 */
export default function throttle(name, limit) {
  const key = `${name}__${limit}`;
  if (!in_throttle[key]) {
    in_throttle[key] = true;

    setTimeout(() => {
      delete in_throttle[key];
    }, limit);
    // function was not throttled, so allow execution
    return true;
  }
  return false;
}

--boundary_.oOo._WgjNqziM8/n9h+MJ1oxF2TyMBp3V3GZh
Content-Length: 1152
Content-Type: application/octet-stream
X-File-MD5: 2ffa37e82381d5086f7ff006ec2368f4
X-File-Mtime: 1718942721
X-File-Path: /DiamondsBucket/CODING/Python-tools/Recompra/.web/utils/helpers/range.js

/**
 * Simulate the python range() builtin function.
 * inspired by https://dev.to/guyariely/using-python-range-in-javascript-337p
 * 
 * If needed outside of an iterator context, use `Array.from(range(10))` or
 * spread syntax `[...range(10)]` to get an array.
 * 
 * @param {number} start: the start or end of the range.
 * @param {number} stop: the end of the range.
 * @param {number} step: the step of the range.
 * @returns {object} an object with a Symbol.iterator method over the range
 */
export default function range(start, stop, step) {
    return {
      [Symbol.iterator]() {
        if (stop === undefined) {
          stop = start;
          start = 0;
        }
        if (step === undefined) {
          step = 1;
        }
  
        let i = start - step;
  
        return {
          next() {
            i += step;
            if ((step > 0 && i < stop) || (step < 0 && i > stop)) {
              return {
                value: i,
                done: false,
              };
            }
            return {
              value: undefined,
              done: true,
            };
          },
        };
      },
    };
  }
--boundary_.oOo._WgjNqziM8/n9h+MJ1oxF2TyMBp3V3GZh
Content-Length: 64
Content-Type: application/octet-stream
X-File-MD5: a5245410b549cd6bd882441adf1aaa6d
X-File-Mtime: 1718944744
X-File-Path: /DiamondsBucket/CODING/Python-tools/Recompra/.web/utils/theme.js

export default {"styles": {"global": {":root": {}, "body": {}}}}
--boundary_.oOo._WgjNqziM8/n9h+MJ1oxF2TyMBp3V3GZh
Content-Length: 45
Content-Type: application/octet-stream
X-File-MD5: deaf8ab1717aeffcfe27c5f2b304e9f7
X-File-Mtime: 1718944744
X-File-Path: /DiamondsBucket/CODING/Python-tools/Recompra/.web/utils/stateful_components.js

/** @jsxImportSource @emotion/react */







--boundary_.oOo._WgjNqziM8/n9h+MJ1oxF2TyMBp3V3GZh
Content-Length: 22762
Content-Type: application/octet-stream
X-File-MD5: 226a45af53eb1a7cfb0f0ef61310219a
X-File-Mtime: 1718942721
X-File-Path: /DiamondsBucket/CODING/Python-tools/Recompra/.web/utils/state.js

// State management for Reflex web apps.
import axios from "axios";
import io from "socket.io-client";
import JSON5 from "json5";
import env from "/env.json";
import Cookies from "universal-cookie";
import { useEffect, useReducer, useRef, useState } from "react";
import Router, { useRouter } from "next/router";
import {
  initialEvents,
  initialState,
  onLoadInternalEvent,
  state_name,
} from "utils/context.js";
import debounce from "/utils/helpers/debounce";
import throttle from "/utils/helpers/throttle";

// Endpoint URLs.
const EVENTURL = env.EVENT;
const UPLOADURL = env.UPLOAD;

// These hostnames indicate that the backend and frontend are reachable via the same domain.
const SAME_DOMAIN_HOSTNAMES = ["localhost", "0.0.0.0", "::", "0:0:0:0:0:0:0:0"];

// Global variable to hold the token.
let token;

// Key for the token in the session storage.
const TOKEN_KEY = "token";

// create cookie instance
const cookies = new Cookies();

// Dictionary holding component references.
export const refs = {};

// Flag ensures that only one event is processing on the backend concurrently.
let event_processing = false;
// Array holding pending events to be processed.
const event_queue = [];

// Pending upload promises, by id
const upload_controllers = {};

/**
 * Generate a UUID (Used for session tokens).
 * Taken from: https://stackoverflow.com/questions/105034/how-do-i-create-a-guid-uuid
 * @returns A UUID.
 */
export const generateUUID = () => {
  let d = new Date().getTime(),
    d2 = (performance && performance.now && performance.now() * 1000) || 0;
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    let r = Math.random() * 16;
    if (d > 0) {
      r = (d + r) % 16 | 0;
      d = Math.floor(d / 16);
    } else {
      r = (d2 + r) % 16 | 0;
      d2 = Math.floor(d2 / 16);
    }
    return (c == "x" ? r : (r & 0x7) | 0x8).toString(16);
  });
};

/**
 * Get the token for the current session.
 * @returns The token.
 */
export const getToken = () => {
  if (token) {
    return token;
  }
  if (typeof window !== "undefined") {
    if (!window.sessionStorage.getItem(TOKEN_KEY)) {
      window.sessionStorage.setItem(TOKEN_KEY, generateUUID());
    }
    token = window.sessionStorage.getItem(TOKEN_KEY);
  }
  return token;
};

/**
 * Get the URL for the backend server
 * @param url_str The URL string to parse.
 * @returns The given URL modified to point to the actual backend server.
 */
export const getBackendURL = (url_str) => {
  // Get backend URL object from the endpoint.
  const endpoint = new URL(url_str);
  if (
    typeof window !== "undefined" &&
    SAME_DOMAIN_HOSTNAMES.includes(endpoint.hostname)
  ) {
    // Use the frontend domain to access the backend
    const frontend_hostname = window.location.hostname;
    endpoint.hostname = frontend_hostname;
    if (window.location.protocol === "https:") {
      if (endpoint.protocol === "ws:") {
        endpoint.protocol = "wss:";
      } else if (endpoint.protocol === "http:") {
        endpoint.protocol = "https:";
      }
      endpoint.port = ""; // Assume websocket is on https port via load balancer.
    }
  }
  return endpoint;
};

/**
 * Apply a delta to the state.
 * @param state The state to apply the delta to.
 * @param delta The delta to apply.
 */
export const applyDelta = (state, delta) => {
  return { ...state, ...delta };
};

/**
 * Handle frontend event or send the event to the backend via Websocket.
 * @param event The event to send.
 * @param socket The socket object to send the event on.
 *
 * @returns True if the event was sent, false if it was handled locally.
 */
export const applyEvent = async (event, socket) => {
  // Handle special events
  if (event.name == "_redirect") {
    if (event.payload.external) {
      window.open(event.payload.path, "_blank");
    } else if (event.payload.replace) {
      Router.replace(event.payload.path);
    } else {
      Router.push(event.payload.path);
    }
    return false;
  }

  if (event.name == "_console") {
    console.log(event.payload.message);
    return false;
  }

  if (event.name == "_remove_cookie") {
    cookies.remove(event.payload.key, { ...event.payload.options });
    queueEvents(initialEvents(), socket);
    return false;
  }

  if (event.name == "_clear_local_storage") {
    localStorage.clear();
    queueEvents(initialEvents(), socket);
    return false;
  }

  if (event.name == "_remove_local_storage") {
    localStorage.removeItem(event.payload.key);
    queueEvents(initialEvents(), socket);
    return false;
  }

  if (event.name == "_set_clipboard") {
    const content = event.payload.content;
    navigator.clipboard.writeText(content);
    return false;
  }

  if (event.name == "_download") {
    const a = document.createElement("a");
    a.hidden = true;
    // Special case when linking to uploaded files
    a.href = event.payload.url.replace("${getBackendURL(env.UPLOAD)}", getBackendURL(env.UPLOAD))
    a.download = event.payload.filename;
    a.