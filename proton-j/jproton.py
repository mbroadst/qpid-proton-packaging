#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from org.apache.qpid.proton.engine import *
from jarray import zeros
from java.util import EnumSet

PN_EOS = Transport.END_OF_STREAM

PN_LOCAL_UNINIT = 1
PN_LOCAL_ACTIVE = 2
PN_LOCAL_CLOSED = 4
PN_REMOTE_UNINIT = 8
PN_REMOTE_ACTIVE = 16
PN_REMOTE_CLOSED = 32

PN_RECEIVED = 1
PN_ACCEPTED = 2
PN_REJECTED = 3
PN_RELEASED = 4
PN_MODIFIED = 5

def enums(mask):
  local = []
  if (PN_LOCAL_UNINIT | mask):
    local.append(EndpointState.UNINITIALIZED)
  if (PN_LOCAL_ACTIVE | mask):
    local.append(EndpointState.ACTIVE)
  if (PN_LOCAL_CLOSED | mask):
    local.append(EndpointState.CLOSED)

  remote = []
  if (PN_REMOTE_UNINIT | mask):
    remote.append(EndpointState.UNINITIALIZED)
  if (PN_REMOTE_ACTIVE | mask):
    remote.append(EndpointState.ACTIVE)
  if (PN_REMOTE_CLOSED | mask):
    remote.append(EndpointState.CLOSED)

  return EnumSet.of(*local), EnumSet.of(*remote)

def state(endpoint):
  local = endpoint.getLocalState()
  remote = endpoint.getRemoteState()

  result = 0

  if (local == EndpointState.UNINITIALIZED):
    result = result | PN_LOCAL_UNINIT
  elif (local == EndpointState.ACTIVE):
    result = result | PN_LOCAL_ACTIVE
  elif (local == EndpointState.CLOSED):
    result = result | PN_LOCAL_CLOSED

  if (remote == EndpointState.UNINITIALIZED):
    result = result | PN_REMOTE_UNINIT
  elif (remote == EndpointState.ACTIVE):
    result = result | PN_REMOTE_ACTIVE
  elif (remote == EndpointState.CLOSED):
    result = result | PN_REMOTE_CLOSED

  return result


def pn_connection():
  return impl.ConnectionImpl()

def pn_connection_destroy(c):
  pass

def pn_connection_state(c):
  return state(c)

def pn_connection_open(c):
  return c.open()

def pn_connection_close(c):
  return c.close()

def pn_session(c):
  return c.session()

def pn_session_destroy(s):
  pass

def pn_session_state(s):
  return state(s)

def pn_session_open(s):
  return s.open()

def pn_session_close(s):
  return s.close()

def pn_transport(c):
  return c.transport()

def pn_trace(t, lvl):
  # XXX: fix up later
  pass

def pn_output(t, size):
  output = zeros(size, "b")
  n = t.output(output, 0, size)
  result = ""
  if n > 0:
    result = output.tostring()[:n]
  return [n, result]

def pn_input(t, inp):
  return t.input(inp, 0, len(inp))

def pn_session_head(c, mask):
  local, remote = enums(mask)
  return c.sessionHead(local, remote)

def pn_sender(ssn, name):
  return ssn.sender(name)

def pn_receiver(ssn, name):
  return ssn.receiver(name)

def pn_link_destroy(lnk):
  pass

def pn_link_state(lnk):
  return state(lnk)

def pn_link_open(lnk):
  return lnk.open()

def pn_link_close(lnk):
  return lnk.close()

def pn_work_head(c):
  return c.getWorkHead()

def pn_flow(rcv, n):
  return rcv.flow(n)

def pn_send(snd, msg):
  return snd.send(msg, 0, len(msg))

def pn_delivery(lnk, tag):
  return lnk.delivery(tag, 0, len(tag))

def pn_delivery_tag(d):
  return d.getTag().tostring()

def pn_writable(d):
  return d.isWritable()

def pn_readable(d):
  return d.isReadable()

def pn_updated(d):
  return d.isUpdated()

def pn_advance(l):
  return l.advance()

def pn_current(l):
  return l.current()

def pn_recv(l, size):
  output = zeros(size, "b")
  n = l.recv(output, 0, size)
  result = ""
  if n > 0:
    result = output.tostring()[:n]
  return [n, result]

def pn_disposition(d, p):
  if p == PN_ACCEPTED:
    d.disposition(Accepted.getInstance())

def pn_remote_disp(d):
  if(d.getRemoteState() == Accepted.getInstance()):
    return PN_ACCEPTED

def pn_local_disp(d):
  if(d.getLocalState() == Accepted.getInstance()):
    return PN_ACCEPTED
