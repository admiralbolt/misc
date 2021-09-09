"""
Script for generating fake invoice data for spreadsheets. This invoice data
represents fake transactions between agents and clients. The invoice data has
the following information:
  * InvoiceID
  * Client Name
  * Client Phone
  * Client Address
  * Client Email
  * Transaction Date
  * SKU#
  * Amount
  * Total Cost (SKU# * Amount)
  * Notes

However there will be a few variations in how the data is stored:
  1. Client Name might be a single field OR a first name / last name.
  2. Client Phone could be in any format.
  3. Transaction Date could be in any format.
  4. Total Cost might be formatted differently as well.
  5. Column order will be randomized.

There are some guarantees though:
  1. We expect the same client to ALWAYS have the same name, phone, address,
     and email.
  2. We expect the InvoiceID to ALWAYS be unique.
  3. We expect the Total Cost to be calculated correctly.

Generation is done by:
  1. Generating random clients.
  2. Generating random items for selling.
  3. Generating random agents.
  4. For each agent, select a random subset to create invoice data.

Each generation creates csv files for each category of data, as well as the
invoice data itself. That's a lot of talking, let's go to work.
"""

import argparse
import csv
import datetime
import hashlib
# Custom library for generating random stuff
import faker
import random

def generate_random_clients(num_clients):
  clients = []
  fake = faker.Faker()
  for _ in range(num_clients):
    clients.append({
      "name": fake.name(),
      "email": fake.email(),
      "address": '"' + fake.address().replace("\n", " ") + '"',
      "phone_number": "".join(map(str, [random.randint(0, 9) for _ in range(10)]))
    })
  return clients

def generate_random_items(num_items):
  items = []
  fake = faker.Faker()
  for i in range(num_items):
    sku = hashlib.md5(bytes(i)).hexdigest()
    items.append({
      "name": fake.bs().title(),
      "sku#": f"SKU#{sku}",
      "cost": f"{round(random.normalvariate(50, 10) + random.randint(-20, 100), 2)}",
      "description": " ".join([fake.sentence() for _ in range(int(random.normalvariate(3, 1)))])
    })
  return items

def generate_random_agents(num_agents):
  agents = []
  fake = faker.Faker()
  for _ in range(num_agents):
    agents.append({
      "name": fake.name(),
      "phone_format": random.choice(["({}) {}-{}", "{}-{}-{}", "{}{}{}"]),
      "date_format": random.choice(["%Y-%m-%d", "%m/%d/%Y"]),
      "dual_name": random.choice([True, False])
    })
  return agents

def generate_invoices(agents, clients, items, num_invoices, num_generations=5):
  """Returns randomly generated invoices in the following structure:
  {
    "agent": {
      "key_order": [...],
      "data": [
          # Generation 0
          [...],
          # Generation 1
          [...]
      ]
    }
  }

  Each generation of data represents an agent accruing more invoices over time.
  Each subsequent generation uses more available clients and items, starting at
  70% and extending up to the full 100% by the last generation.
  """
  invoices = {}
  fake = faker.Faker()
  for i, agent in enumerate(agents):
    all_keys = ["invoice_id", "phone_number", "address", "email", "date", "sku#", "amount", "total_cost"]
    if agent["dual_name"]:
      all_keys.extend(["first_name", "last_name"])
    else:
      all_keys.append("name")
    random.shuffle(all_keys)
    invoices[agent["name"]] = {
      "key_order": all_keys,
      "generations": []
    }

    all_invoice_data = []
    for j in range(num_invoices):
      iid = hashlib.md5(bytes(1000 + 13 * (i * num_invoices + j))).hexdigest()
      client = random.choice(clients)
      item = random.choice(items)
      amount = int(random.normalvariate(5, 2) + random.randint(1, 10) + random.randint(1, 10))
      total = amount * float(item["cost"])
      invoice = {
        "invoice_id": f"IID#{iid}",
        "phone_number": agent["phone_format"].format(
          client["phone_number"][:3], client["phone_number"][3:6], client["phone_number"][6:]
        ),
        "address": client["address"],
        "email": client["email"],
        "date": fake.date_between("-5y").strftime(agent["date_format"]),
        "sku#":  item["sku#"],
        "amount": f"{amount}",
        "total_cost": f"{total}"
      }
      if agent["dual_name"]:
        invoice["first_name"] = client["name"].split()[0]
        invoice["last_name"] = client["name"].split()[1]
      else:
        invoice["name"] = client["name"]
      all_invoice_data.append(invoice)
    all_invoice_data.sort(key=lambda item: datetime.datetime.strptime(item["date"], agent["date_format"]))
    generations = []
    for i in range(num_generations):
      index = round(0.7 * num_invoices + ((i + 1) / (num_generations)) * 0.3 * num_invoices)
      generations.append(all_invoice_data[:index])
    invoices[agent["name"]]["generations"] = generations
  return invoices

def write_csv(file_name, key_order, data):
  with open(file_name, "w") as wh:
    wh.write(",".join([key.replace("_", " ").title() for key in key_order]) + "\n")
    for row in data:
      wh.write(",".join([row[key] for key in key_order]) + "\n")


def main():
  parser = argparse.ArgumentParser(description="Generate random invoice data!")
  parser.add_argument("--agents", type=int, default=10, help="The number of agents to generate data for.")
  parser.add_argument("--clients", type=int, default=1000, help="The number of fake clients to generate.")
  parser.add_argument("--items", type=int, default=1000, help="The number of fake items we are selling.")
  parser.add_argument("--invoices", type=int, default=500, help="The average number of invoices per agent.")
  args = parser.parse_args()

  clients = generate_random_clients(args.clients)
  write_csv("invoice_data/clients.csv", ["name", "email", "address", "phone_number"], clients)

  items = generate_random_items(args.items)
  write_csv("invoice_data/items.csv", ["name", "sku#", "cost", "description"], items)

  agents = generate_random_agents(args.agents)
  write_csv("invoice_data/agents.csv", ["name"], agents)

  invoices = generate_invoices(agents, clients, items, args.invoices)
  for agent, invoice_info in invoices.items():
    agent_name = agent.replace(" ", "").lower()
    for i, gen in enumerate(invoice_info["generations"]):
      write_csv(f"invoice_data/invoices_per_agent/{agent_name}_{i}.csv", invoice_info["key_order"], gen)

if __name__ == "__main__":
  main()
