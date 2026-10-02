import type {Server} from 'node:http';
export function contextOnly(input:unknown):Record<string,string>;
export function advicePrompt(context:unknown):string;
export function acceptAdvice(value:unknown):string;
export function createAdviceServer():Server;
