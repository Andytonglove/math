import test from "node:test";
import assert from "node:assert/strict";
import {resolve,join} from "node:path";
import {readFileSync,existsSync} from "node:fs";
import {validateTasks} from "../scripts/validate_pilot.mjs";
test("task evidence anchors are present in forked source",()=>{
  const root=resolve(".");
  const filename=join(root,"research/proof_understanding/evaluation/pilot_tasks.json");
  assert.ok(existsSync(filename),"Run from repo root with the pilot tasks checked out");
  const items=JSON.parse(readFileSync(filename,"utf8"));
  const result=validateTasks(root,items);
  assert.deepEqual(result.errors,[]);
  assert.equal(result.total,5);
  assert.equal(result.source_grounded,4);
  assert.equal(result.oracle_pending,1);
});
test("pending items cannot advertise a gold label",()=>{
 const bad=[{id:"bad",status:"oracle_pending",oracle_label:"true",evidence:[{file:"README.md",anchor:"# Readme"}]}];
 assert.ok(validateTasks(resolve("."),bad).errors.some(e=>e.includes("unscored")));
});
